from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient, ContentSettings, generate_blob_sas, BlobSasPermissions
import clearance.settings as settings
import os, datetime, subprocess
import gdal2tiles
from osgeo import gdal

storage_account_key = settings.STORAGE_ACCOUNT_KEY
storage_account_name = settings.AZURE_ACCOUNT_NAME
connection_string = settings.CONNECTION_STRING
container_name = "media"

blob_service_cl = BlobServiceClient.from_connection_string(conn_str=connection_string)
container_client = blob_service_cl.get_container_client(container=container_name)

def list_blobs(dir):
    dir = settings.PROJECT_NAME +'/' + dir
    blob_names = container_client.list_blob_names(name_starts_with=dir)
    return blob_names

def list_blob_data(dir):
    dir = settings.PROJECT_NAME +'/' + dir
    blobs = container_client.list_blobs(name_starts_with=dir)
    return blobs

def overwrite_tr(itp_no_mag):
    duplicates = list_blobs(os.path.join('media/targetrecords', itp_no_mag+'('))
    for duplicate in duplicates:
      blob_service_cl.get_blob_client(container=container_name, blob=duplicate).delete_blob()

def save_pdf(file_path, file_name):
    file_name = settings.PROJECT_NAME + '/' + file_name
    with open(file_path, mode='rb') as data:
      container_client.upload_blob(name=file_name, data=data, overwrite=True)
    os.remove(file_path)

def save_img(file_path, file_name):
    file_name = settings.PROJECT_NAME + '/' + file_name
    with open(file_path, mode='rb') as data:
      container_client.upload_blob(name=file_name, data=data, overwrite=True)
    os.remove(file_path)

def delete_img(itp_no_mag):
    imgs = list_blobs(os.path.join('media/mtlimages', itp_no_mag+'_'))
    for img in imgs:
      blob_service_cl.get_blob_client(container=container_name, blob=img).delete_blob()

def delete_file(path):
  blob_service_cl.get_blob_client(container=container_name, blob=path).delete_blob()
 
def overwrite_duplicate(instance, filename, dir):
    if os.path.join(settings.PROJECT_NAME, dir, filename) in list_blobs(dir):
      blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
      blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.join(settings.PROJECT_NAME, dir, filename))
      blob_client.delete_blob()
    return os.path.join(settings.PROJECT_NAME, dir, filename)
    #not overwriting mbes.tif

def remove_contents_of_directory(directory_path):
  for entry in os.listdir(directory_path):
      entry_path = os.path.join(directory_path, entry)

      if os.path.isfile(entry_path):
          os.remove(entry_path)
      elif os.path.isdir(entry_path):
          remove_contents_of_directory(entry_path)

#Function assumes sss and tmi are single band rasters with color tables, while mbes is rgb image
#Function assumes sss is grayscale
def upload_xyz(type):
    subprocess.run(['wget', settings.MEDIA_URL + settings.PROJECT_NAME +'/geodata/tiff/'+type+".tif", '-O', "tmp/tmp.tif"])
    target_projection = 'EPSG:'+str(settings.EPSG)
    
    if type == "mbes":
      create_mask_command = [
        'gdal_translate',
        '-of', 'GTiff',
        '-b', '1', '-b', '2', '-b', '3',
        '-a_nodata', '255',
        'tmp/tmp.tif',
        'tmp/tmp_masked.tif'
      ]
      subprocess.run(create_mask_command)
    else:
      create_mask_command = [
        'gdal_translate',
        '-of', 'GTiff',
        '-b', '1',
        '-a_nodata', '255',
        'tmp/tmp.tif',
        'tmp/tmp_masked.tif'
      ]
      subprocess.run(create_mask_command)
    
    if type == 'tmi':
      command = [
        'gdal_translate',
        '-of', 'vrt',
        '-a_srs', target_projection,
        '-expand', 'rgba',
        'tmp/tmp_masked.tif',
        'tmp/temp.vrt'
      ]
      subprocess.run(command)
      gdal2tiles.generate_tiles("tmp/temp.vrt", 'tmp/xyz', nb_processes=2, zoom='0-18')
    elif type == 'mbes':
      command = [
        'gdal_translate',
        '-of', 'vrt',
        '-a_srs', target_projection,
        #'-expand', 'rgba',
        'tmp/tmp_masked.tif',
        'tmp/temp.vrt'
      ]
      subprocess.run(command)
      gdal2tiles.generate_tiles("tmp/temp.vrt", 'tmp/xyz', nb_processes=2, zoom='0-18')
    elif type == 'sss':
      command = [
        'gdal_translate',
        '-of', 'vrt',
        '-a_srs', target_projection,
        'tmp/tmp_masked.tif',
        'tmp/temp.vrt'
      ]
      subprocess.run(command)
      gdal2tiles.generate_tiles("tmp/temp.vrt", 'tmp/xyz', nb_processes=2, zoom='0-18')

    os.remove("tmp/tmp.tif")
    os.remove('tmp/tmp_masked.tif')

    for root, dirs, files in os.walk('tmp/xyz'):
      for local_file in files:
        local_file_path = os.path.join(root, local_file)
        relative_path = os.path.relpath(local_file_path, 'tmp/xyz')
        azure_blob_name = os.path.join(settings.PROJECT_NAME +'/geodata/tiles/'+type, relative_path).replace(os.path.sep, "/")

        #blob_client = blob_service_cl.get_blob_client(container=container_name, blob=azure_blob_name)

        with open(local_file_path, "rb") as data:
            container_client.upload_blob(data=data, name=azure_blob_name, overwrite=True)

    remove_contents_of_directory('tmp/xyz')

def get_secure_blob_url(name):
  sas_token = generate_blob_sas(
    account_name=blob_service_cl.account_name,
    container_name=container_name,
    blob_name=name,
    account_key=blob_service_cl.credential.account_key,
    permission=BlobSasPermissions(read=True),
    expiry=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
  )

  return f"https://{blob_service_cl.account_name}.blob.core.windows.net/{container_name}/{name}?{sas_token}"