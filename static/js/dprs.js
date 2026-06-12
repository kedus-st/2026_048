document.addEventListener('DOMContentLoaded', function() {
    
    document.getElementById('selected-report-date').value = new Date().toISOString().slice(0, 10);
    getReport(document.getElementById('selected-report-date').value);
    document.getElementById('selected-report-date').addEventListener('change', function() {
        date = this.value;
        getReport(date);
    });
    document.getElementById('save-report-button').addEventListener('click', function() {
        saveReport();
    });
    document.getElementById('reload-totals').addEventListener('click', function() {
        reloadTotals(document.getElementById('selected-report-date').value);
    });
    document.getElementById('reset-dpr').addEventListener('click', function() {
        resetDPR(document.getElementById('selected-report-date').value);
    });
    document.getElementById('generate-dpr-pdf').addEventListener('click', () => {
        printDPR(document.getElementById('selected-report-date').value);
    });
    document.getElementById("copy-dpr").addEventListener("click", () => {
        copyDPR();
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function getReport(date) {
        fetch('/dprs/get-report?date=' + encodeURIComponent(date))
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById('ceo_name').innerText = data.ceo.name || '';
                document.getElementById('ceo_number').innerText = data.ceo.number || '';
                document.getElementById('pm_name').innerText = data.project_manager.name || '';
                document.getElementById('pm_number').innerText = data.project_manager.number || '';
                document.getElementById('ocm_name').innerText = data.ocm.name || '';
                document.getElementById('ocm_number').innerText = data.ocm.number || '';
                document.getElementById('eodm_name').innerText = data.eod_manager.name || '';
                document.getElementById('eodm_number').innerText = data.eod_manager.number || '';
                document.getElementById('captain_name').innerText = data.captain.name || '';
                document.getElementById('captain_number').innerText = data.captain.number || '';
                document.getElementById('clientrep_name').innerText = data.client_rep.name || '';
                document.getElementById('clientrep_number').innerText = data.client_rep.number || '';
                document.getElementById('vessel_email').innerText = data.vessel_email || '';

                document.getElementById('vessel_position').innerText = data.position_at_2400 || '';

                const distListContainer = document.getElementById('distribution-list-entries');
                distListContainer.innerHTML = '';
                if (data.distribution_list && data.distribution_list.length > 0) {
                    data.distribution_list.forEach(entry => {
                        const template = document.getElementById('distribution-list-template-entry');
                        const newEntry = template.content.cloneNode(true);
                        const row = newEntry.querySelector('.form-row');
                        row.querySelector('.entry-text').textContent = entry;
                        row.querySelector('.remove-row').addEventListener('click', function () {
                            this.closest('.form-row').remove();
                        });
                        distListContainer.appendChild(newEntry);
                    });
                }
                document.getElementById('add-distribution-list-entry').addEventListener('click', function() {
                    const template = document.getElementById('distribution-list-template-entry');
                    const newEntry = template.content.cloneNode(true);
                    const row = newEntry.querySelector('.form-row');
                    row.querySelector('.remove-row').addEventListener('click', function () {
                        this.closest('.form-row').remove();
                    });
                    distListContainer.appendChild(newEntry);
                });

                const marineOnsigners = document.getElementById('marine-onsigners-list');
                marineOnsigners.innerHTML = '';
                if (data.marine_onsigners && data.marine_onsigners.length > 0) {
                    data.marine_onsigners.forEach(entry => {
                        const template = document.getElementById('personnel-list-template-entry');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelector('.entry-text').textContent = entry;
                        marineOnsigners.appendChild(newEntry);
                    });
                }
                document.getElementById('add-marine-onsigner').addEventListener('click', function() {
                    const template = document.getElementById('personnel-list-template-entry');
                    const newEntry = template.content.cloneNode(true);
                    marineOnsigners.appendChild(newEntry);
                });
                const seaterraOnsigners = document.getElementById('seaterra-onsigners-list');
                seaterraOnsigners.innerHTML = '';
                if (data.seaterra_onsigners && data.seaterra_onsigners.length > 0) {
                    data.seaterra_onsigners.forEach(entry => {
                        const template = document.getElementById('personnel-list-template-entry');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelector('.entry-text').textContent = entry;
                        seaterraOnsigners.appendChild(newEntry);
                    });
                }
                document.getElementById('add-seaterra-onsigner').addEventListener('click', function() {
                    const template = document.getElementById('personnel-list-template-entry');
                    const newEntry = template.content.cloneNode(true);
                    seaterraOnsigners.appendChild(newEntry);
                });
                const client_onsigners = document.getElementById('client-onsigners-list');
                client_onsigners.innerHTML = '';
                if (data.client_onsigners && data.client_onsigners.length > 0) {
                    data.client_onsigners.forEach(entry => {
                        const template = document.getElementById('personnel-list-template-entry');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelector('.entry-text').textContent = entry;
                        client_onsigners.appendChild(newEntry);
                    });
                }
                document.getElementById('add-client-onsigner').addEventListener('click', function() {
                    const template = document.getElementById('personnel-list-template-entry');
                    const newEntry = template.content.cloneNode(true);
                    client_onsigners.appendChild(newEntry);
                });

                const marine_offsigners = document.getElementById('marine-offsigners-list');
                marine_offsigners.innerHTML = '';
                if (data.marine_offsigners && data.marine_offsigners.length > 0) {
                    data.marine_offsigners.forEach(entry => {
                        const template = document.getElementById('personnel-list-template-entry');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelector('.entry-text').textContent = entry;
                        marine_offsigners.appendChild(newEntry);
                    });
                }
                document.getElementById('add-marine-offsigner').addEventListener('click', function() {
                    const template = document.getElementById('personnel-list-template-entry');
                    const newEntry = template.content.cloneNode(true);
                    marine_offsigners.appendChild(newEntry);
                });
                const seaterra_offsigners = document.getElementById('seaterra-offsigners-list');
                seaterra_offsigners.innerHTML = '';
                if (data.seaterra_offsigners && data.seaterra_offsigners.length > 0) {
                    data.seaterra_offsigners.forEach(entry => {
                        const template = document.getElementById('personnel-list-template-entry');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelector('.entry-text').textContent = entry;
                        seaterra_offsigners.appendChild(newEntry);
                    });
                }
                document.getElementById('add-seaterra-offsigner').addEventListener('click', function() {
                    const template = document.getElementById('personnel-list-template-entry');
                    const newEntry = template.content.cloneNode(true);
                    seaterra_offsigners.appendChild(newEntry);
                });
                const client_offsigners = document.getElementById('client-offsigners-list');
                client_offsigners.innerHTML = '';
                if (data.client_offsigners && data.client_offsigners.length > 0) {
                    data.client_offsigners.forEach(entry => {
                        const template = document.getElementById('personnel-list-template-entry');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelector('.entry-text').textContent = entry;
                        client_offsigners.appendChild(newEntry);
                    });
                }
                document.getElementById('add-client-offsigner').addEventListener('click', function() {
                    const template = document.getElementById('personnel-list-template-entry');
                    const newEntry = template.content.cloneNode(true);
                    client_offsigners.appendChild(newEntry);
                });

                weatherEntries = document.getElementById('weather-entries');
                weatherEntries.innerHTML = '';
                if (data.weather_info && data.weather_info.length > 0) {
                    data.weather_info.forEach(entry => {
                        const template = document.getElementById('weather-entry-template');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelectorAll('.entry-text')[0].textContent = entry.time;
                        newEntry.querySelectorAll('.entry-text')[1].textContent = entry.max_wave_today;
                        newEntry.querySelectorAll('.entry-text')[2].textContent = entry.max_wave_tomorrow;
                        weatherEntries.appendChild(newEntry);
                    });
                }
                weatherLookahead = document.getElementById('weather-lookahead-entries');
                weatherLookahead.innerHTML = '';
                if (data.weather_info_lookahead && data.weather_info_lookahead.length > 0) {
                    data.weather_info_lookahead.forEach(entry => {
                        const template = document.getElementById('weather-entry-template');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelectorAll('.entry-text')[0].textContent = entry.time;
                        newEntry.querySelectorAll('.entry-text')[1].textContent = entry['48hrs'];
                        newEntry.querySelectorAll('.entry-text')[2].textContent = entry['72hrs'];
                        weatherLookahead.appendChild(newEntry);
                    });
                }

                document.getElementById('daily_meetings_today').innerText = data.hse_meetings || '';
                document.getElementById('toolbox_talks_today').innerText = data.hse_toolbox_talks || '';
                document.getElementById('safety_observation_form_today').innerText = data.hse_safety_observation_form || '';
                document.getElementById('safety_drills_today').innerText = data.hse_safety_drills || '';
                document.getElementById('incidents_today').innerText = data.hse_incidents || '';
                document.getElementById('accidents_today').innerText = data.hse_accidents || '';
                document.getElementById('working_hours_today').innerText = data.hse_working_hours || '';
                document.getElementById('project_start').innerText = data.hse_start || '';
                document.getElementById('days_without_accident').innerText = data.hse_days_without_accident || '';

                document.getElementById('daily_meetings_total').innerText = data.hse_meetings_total || '';
                document.getElementById('daily_meetings_total').setAttribute('source_val', data.previous_hse_meetings_total || '0');
                document.getElementById('toolbox_talks_total').innerText = data.hse_toolbox_talks_total || '';
                document.getElementById('toolbox_talks_total').setAttribute('source_val', data.previous_hse_toolbox_talks_total || '0');
                document.getElementById('safety_observation_form_total').innerText = data.hse_safety_observation_form_total || '';
                document.getElementById('safety_observation_form_total').setAttribute('source_val', data.previous_hse_safety_observation_form_total || '0');
                document.getElementById('safety_drills_total').innerText = data.hse_safety_drills_total || '';
                document.getElementById('safety_drills_total').setAttribute('source_val', data.previous_hse_safety_drills_total || '0');
                document.getElementById('incidents_total').innerText = data.hse_incidents_total || '';
                document.getElementById('incidents_total').setAttribute('source_val', data.previous_hse_incidents_total || '0');
                document.getElementById('accidents_total').innerText = data.hse_accidents_total || '';
                document.getElementById('accidents_total').setAttribute('source_val', data.previous_hse_accidents_total || '0');
                document.getElementById('working_hours_total').innerText = data.hse_working_hours_total || '';
                document.getElementById('working_hours_total').setAttribute('source_val', data.previous_hse_working_hours_total || '0');
                document.getElementById('days_since_start').innerText = data.hse_days_since_start || '';
                document.getElementById('days_without_accident_total').innerText = data.hse_days_without_accident_total || '';
                document.getElementById('days_without_accident_total').setAttribute('source_val', data.previous_hse_days_without_accident_total || '0');

                document.getElementById('work_summary').innerText = data.work_summary || '';
                workEntries = document.getElementById('work_entries');
                workEntries.innerHTML = '';
                if (data.work_entries && data.work_entries.length > 0) {
                    data.work_entries.forEach(entry => {
                        const template = document.getElementById('work-entry-template');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelectorAll('.entry-text')[0].textContent = entry.target_id;
                        newEntry.querySelectorAll('.entry-text')[1].textContent = entry.description;
                        newEntry.querySelectorAll('.entry-text')[2].textContent = entry.object;
                        workEntries.appendChild(newEntry);
                    });
                }
                document.getElementById('add-work-entry').addEventListener('click', function() {
                    const template = document.getElementById('work-entry-template');
                    const newEntry = template.content.cloneNode(true);
                    workEntries.appendChild(newEntry);
                });

                document.getElementById('plan_for_next_24hrs').innerText = data.plan_24hrs || '';

                dailyRoutine = document.getElementById('daily-routine-entries');
                dailyRoutine.innerHTML = '';
                if (data.daily_routine && data.daily_routine.length > 0) {
                    data.daily_routine.forEach(entry => {
                        const template = document.getElementById('daily-routine-template');
                        const newEntry = template.content.cloneNode(true);
                        newEntry.querySelectorAll('.entry-text')[0].textContent = entry.from;
                        newEntry.querySelectorAll('.entry-text')[1].textContent = entry.to;
                        newEntry.querySelectorAll('.entry-text')[2].textContent = entry.duration;
                        newEntry.querySelectorAll('select')[0].value = entry.category;
                        newEntry.querySelectorAll('.entry-text')[3].textContent = entry.target_id;
                        newEntry.querySelectorAll('.entry-text')[4].textContent = entry.description;
                        dailyRoutine.appendChild(newEntry);
                    })
                }
                document.getElementById('add-daily-routine-entry').addEventListener('click', function() {
                    const template = document.getElementById('daily-routine-template');
                    const newEntry = template.content.cloneNode(true);
                    dailyRoutine.appendChild(newEntry);
                });
                
                document.getElementById('routine_vessel').textContent = data.routine_vessel || '';
                document.getElementById('routine_total_targets').textContent = data.routine_total_targets || '';
                document.getElementById('routine_cleared_targets').textContent = data.routine_cleared_targets || '';
                document.getElementById('routine_remaining_targets').textContent = data.routine_remaining_targets || '';
                document.getElementById('routine_total_uxos_found').textContent = data.routine_total_uxos_found || '';
                document.getElementById('routine_targets_cleared_today').textContent = data.routine_targets_cleared_today || '';
                document.getElementById('routine_remarks').textContent = data.routine_remarks || '';

                document.getElementById('previous_mob_time').textContent = data.previous_mob_time || '';
                document.getElementById('previous_t_time').textContent = data.previous_t_time || '';
                document.getElementById('previous_i_time').textContent = data.previous_i_time || '';
                document.getElementById('previous_cs_time').textContent = data.previous_cs_time || '';
                document.getElementById('previous_wdt_time').textContent = data.previous_wdt_time || '';
                document.getElementById('previous_tbw_time').textContent = data.previous_tbw_time || '';
                document.getElementById('previous_cc_time').textContent = data.previous_cc_time || '';
                document.getElementById('previous_tdt_time').textContent = data.previous_tdt_time || '';
                document.getElementById('previous_total_time').textContent = data.previous_total_time || '';

                document.getElementById('today_mob_time').textContent = data.mob_duration || '';
                document.getElementById('today_t_time').textContent = data.t_duration || '';
                document.getElementById('today_i_time').textContent = data.i_duration || '';
                document.getElementById('today_cs_time').textContent = data.cs_duration || '';
                document.getElementById('today_wdt_time').textContent = data.wdt_duration || '';
                document.getElementById('today_tbw_time').textContent = data.tbw_duration || '';
                document.getElementById('today_cc_time').textContent = data.cc_duration || '';
                document.getElementById('today_tdt_time').textContent = data.tdt_duration || '';
                document.getElementById('today_total_time').textContent = data.total_duration || '';

                document.getElementById('accumulated_mob_time').textContent = data.mob_duration_total || '';
                document.getElementById('accumulated_mob_time').setAttribute('source_val', data.previous_mob_duration_total || '0');
                document.getElementById('accumulated_t_time').textContent = data.t_duration_total || '';
                document.getElementById('accumulated_t_time').setAttribute('source_val', data.previous_t_duration_total || '0');
                document.getElementById('accumulated_i_time').textContent = data.i_duration_total || '';
                document.getElementById('accumulated_i_time').setAttribute('source_val', data.previous_i_duration_total || '0');
                document.getElementById('accumulated_cs_time').textContent = data.cs_duration_total || '';
                document.getElementById('accumulated_cs_time').setAttribute('source_val', data.previous_cs_duration_total || '0');
                document.getElementById('accumulated_wdt_time').textContent = data.wdt_duration_total || '';
                document.getElementById('accumulated_wdt_time').setAttribute('source_val', data.previous_wdt_duration_total || '0');
                document.getElementById('accumulated_tbw_time').textContent = data.tbw_duration_total || '';
                document.getElementById('accumulated_tbw_time').setAttribute('source_val', data.previous_tbw_duration_total || '0');
                document.getElementById('accumulated_cc_time').textContent = data.cc_duration_total || '';
                document.getElementById('accumulated_cc_time').setAttribute('source_val', data.previous_cc_duration_total || '0');
                document.getElementById('accumulated_tdt_time').textContent = data.tdt_duration_total || '';
                document.getElementById('accumulated_tdt_time').setAttribute('source_val', data.previous_tdt_duration_total || '0');
                document.getElementById('accumulated_total_time').textContent = data.total_duration_total || '';
                document.getElementById('accumulated_total_time').setAttribute('source_val', data.previous_total_duration_total || '0');

                document.getElementById('weather_interpretation').textContent = data.weather_interpretation || '';
                document.getElementById('technical_issues').textContent = data.technical_issues || '';
                document.getElementById('meetings').textContent = data.meetings || '';
                document.getElementById('other_remarks').textContent = data.other_remarks || '';

                document.getElementById('client_comments').textContent = data.client_comments || '';
                document.getElementById('seaterra_comments').textContent = data.seaterra_comments || '';
            })
        .catch(error => {
            console.error('Error fetching report:', error);
        });
    }

    function saveReport() {
        date = document.getElementById('selected-report-date').value;
        //vessel = document.getElementById('vessel').innerText;
        position_at_2400 = document.getElementById('vessel_position').innerText;

        ceo = {"name": document.getElementById('ceo_name').innerText, "number": document.getElementById('ceo_number').innerText};
        project_manager = {"name": document.getElementById('pm_name').innerText, "number": document.getElementById('pm_number').innerText};
        ocm = {"name": document.getElementById('ocm_name').innerText, "number": document.getElementById('ocm_number').innerText};
        eod_manager = {"name": document.getElementById('eodm_name').innerText, "number": document.getElementById('eodm_number').innerText};
        captain = {"name": document.getElementById('captain_name').innerText, "number": document.getElementById('captain_number').innerText};
        client_rep = {"name": document.getElementById('clientrep_name').innerText, "number": document.getElementById('clientrep_number').innerText};
        vessel_email = document.getElementById('vessel_email').innerText;

        const distribution_list = [];
        document.querySelectorAll('#distribution-list-entries .entry-text').forEach(entry => {
            if (entry.textContent.trim() !== '') {
                distribution_list.push(entry.textContent.trim());
            }
        });
        const marine_onsigners = [];
        document.querySelectorAll('#marine-onsigners-list .entry-text').forEach(entry => {
            if (entry.textContent.trim() !== '') {
                marine_onsigners.push(entry.textContent.trim());
            }
        });
        const seaterra_onsigners = [];
        document.querySelectorAll('#seaterra-onsigners-list .entry-text').forEach(entry => {
            if (entry.textContent.trim() !== '') {
                seaterra_onsigners.push(entry.textContent.trim());
            }
        });
        const client_onsigners = [];
        document.querySelectorAll('#client-onsigners-list .entry-text').forEach(entry => {
            if (entry.textContent.trim() !== '') {
                client_onsigners.push(entry.textContent.trim());
            }
        });
        const marine_offsigners = [];
        document.querySelectorAll('#marine-offsigners-list .entry-text').forEach(entry => {
            if (entry.textContent.trim() !== '') {
                marine_offsigners.push(entry.textContent.trim());
            }
        });
        const seaterra_offsigners = [];
        document.querySelectorAll('#seaterra-offsigners-list .entry-text').forEach(entry => {
            if (entry.textContent.trim() !== '') {
                seaterra_offsigners.push(entry.textContent.trim());
            }
        });
        const client_offsigners = [];
        document.querySelectorAll('#client-offsigners-list .entry-text').forEach(entry => {
            if (entry.textContent.trim() !== '') {
                client_offsigners.push(entry.textContent.trim());
            }
        });
    
        weather_info = [];
        document.querySelectorAll('#weather-entries .form-row').forEach(entry => {
            time = entry.querySelectorAll('.entry-text')[0].textContent.trim();
            max_wave_today = entry.querySelectorAll('.entry-text')[1].textContent.trim();
            max_wave_tomorrow = entry.querySelectorAll('.entry-text')[2].textContent.trim();
            weather_info.push({
                time: time,
                max_wave_today: max_wave_today,
                max_wave_tomorrow: max_wave_tomorrow
            });
        });

        weather_info_lookahead = [];
        document.querySelectorAll('#weather-lookahead-entries .form-row').forEach(entry => {
            time = entry.querySelectorAll('.entry-text')[0].textContent.trim();
            wave_48hrs = entry.querySelectorAll('.entry-text')[1].textContent.trim();
            weather_info_lookahead.push({
                time: time,
                wave_48hrs: wave_48hrs
            });
        });

        hse_meetings = document.getElementById('daily_meetings_today').innerText;
        hse_toolbox_talks = document.getElementById('toolbox_talks_today').innerText;
        hse_safety_observation_form = document.getElementById('safety_observation_form_today').innerText;
        hse_safety_drills = document.getElementById('safety_drills_today').innerText;
        hse_incidents = document.getElementById('incidents_today').innerText;
        hse_accidents = document.getElementById('accidents_today').innerText;
        hse_working_hours = document.getElementById('working_hours_today').innerText;
        hse_start = document.getElementById('project_start').innerText;
        hse_days_without_accident = document.getElementById('days_without_accident').innerText;

        hse_meetings_total = document.getElementById('daily_meetings_total').innerText;
        hse_toolbox_talks_total = document.getElementById('toolbox_talks_total').innerText;
        hse_safety_observation_form_total = document.getElementById('safety_observation_form_total').innerText;
        hse_safety_drills_total = document.getElementById('safety_drills_total').innerText;
        hse_incidents_total = document.getElementById('incidents_total').innerText;
        hse_accidents_total = document.getElementById('accidents_total').innerText;
        hse_working_hours_total = document.getElementById('working_hours_total').innerText;
        hse_days_without_accident_total = document.getElementById('days_without_accident_total').innerText;

        work_summary = document.getElementById('work_summary').innerText;
        const work_entries = [];
        document.querySelectorAll('#work_entries .form-row').forEach(entry => {
            target_id = entry.querySelectorAll('.entry-text')[0].textContent.trim();
            description = entry.querySelectorAll('.entry-text')[1].textContent.trim();
            object = entry.querySelectorAll('.entry-text')[2].textContent.trim();
            work_entries.push({
                target_id: target_id,
                description: description,
                object: object
            });
        });

        plan_24hrs = document.getElementById('plan_for_next_24hrs').innerText;
        
        const daily_routine = [];
        document.querySelectorAll('#daily-routine-entries .form-row').forEach(entry => {
            from = entry.querySelectorAll('.entry-text')[0].textContent.trim();
            to = entry.querySelectorAll('.entry-text')[1].textContent.trim();
            duration = entry.querySelectorAll('.entry-text')[2].textContent.trim();
            category = entry.querySelectorAll('select')[0].value;
            target_id = entry.querySelectorAll('.entry-text')[3].textContent.trim();
            description = entry.querySelectorAll('.entry-text')[4].textContent.trim();
            daily_routine.push({
                from: from,
                to: to,
                duration: duration,
                category: category,
                target_id: target_id,
                description: description
            });
        });

        routine_vessel = document.getElementById('routine_vessel').textContent;
        routine_total_targets = document.getElementById('routine_total_targets').textContent;
        routine_cleared_targets = document.getElementById('routine_cleared_targets').textContent;
        routine_remaining_targets = document.getElementById('routine_remaining_targets').textContent;
        routine_total_uxos_found = document.getElementById('routine_total_uxos_found').textContent;
        routine_targets_cleared_today = document.getElementById('routine_targets_cleared_today').textContent;
        routine_remarks = document.getElementById('routine_remarks').textContent;
        
        mob_duration = document.getElementById('today_mob_time').textContent;
        t_duration = document.getElementById('today_t_time').textContent;
        i_duration = document.getElementById('today_i_time').textContent;
        cs_duration = document.getElementById('today_cs_time').textContent;
        wdt_duration = document.getElementById('today_wdt_time').textContent;
        tbw_duration = document.getElementById('today_tbw_time').textContent;
        cc_duration = document.getElementById('today_cc_time').textContent;
        tdt_duration = document.getElementById('today_tdt_time').textContent;
        total_duration = document.getElementById('today_total_time').textContent;

        mob_duration_total = document.getElementById('accumulated_mob_time').textContent;
        t_duration_total = document.getElementById('accumulated_t_time').textContent;
        i_duration_total = document.getElementById('accumulated_i_time').textContent;
        cs_duration_total = document.getElementById('accumulated_cs_time').textContent;
        wdt_duration_total = document.getElementById('accumulated_wdt_time').textContent;
        tbw_duration_total = document.getElementById('accumulated_tbw_time').textContent;
        cc_duration_total = document.getElementById('accumulated_cc_time').textContent;
        tdt_duration_total = document.getElementById('accumulated_tdt_time').textContent;
        total_duration_total = document.getElementById('accumulated_total_time').textContent;

        weather_interpretation = document.getElementById('weather_interpretation').textContent;
        technical_issues = document.getElementById('technical_issues').textContent;
        meetings = document.getElementById('meetings').textContent;
        other_remarks = document.getElementById('other_remarks').textContent;

        client_comments = document.getElementById('client_comments').textContent;
        seaterra_comments = document.getElementById('seaterra_comments').textContent;

        const payload = {
            date: date,
            ceo: ceo,
            project_manager: project_manager,
            ocm: ocm,
            eod_manager: eod_manager,
            captain: captain,
            client_rep: client_rep,
            vessel_email: vessel_email,
            position_at_2400: position_at_2400,
            distribution_list: distribution_list,
            marine_onsigners: marine_onsigners,
            seaterra_onsigners: seaterra_onsigners,
            client_onsigners: client_onsigners,
            marine_offsigners: marine_offsigners,
            seaterra_offsigners: seaterra_offsigners,
            client_offsigners: client_offsigners,
            weather_info: weather_info,
            weather_info_lookahead: weather_info_lookahead,
            hse_meetings: hse_meetings,
            hse_toolbox_talks: hse_toolbox_talks,
            hse_safety_observation_form: hse_safety_observation_form,
            hse_safety_drills: hse_safety_drills,
            hse_incidents: hse_incidents,
            hse_accidents: hse_accidents,
            hse_working_hours: hse_working_hours,
            hse_start: hse_start,
            hse_days_without_accident: hse_days_without_accident,
            hse_meetings_total: hse_meetings_total,
            hse_toolbox_talks_total: hse_toolbox_talks_total,
            hse_safety_observation_form_total: hse_safety_observation_form_total,
            hse_safety_drills_total: hse_safety_drills_total,
            hse_incidents_total: hse_incidents_total,
            hse_accidents_total: hse_accidents_total,
            hse_working_hours_total: hse_working_hours_total,
            hse_days_without_accident_total: hse_days_without_accident_total,
            work_summary: work_summary,
            work_entries: work_entries,
            plan_24hrs: plan_24hrs,
            daily_routine: daily_routine,
            routine_vessel: routine_vessel,
            routine_total_targets: routine_total_targets,
            routine_cleared_targets: routine_cleared_targets,
            routine_remaining_targets: routine_remaining_targets,
            routine_total_uxos_found: routine_total_uxos_found,
            routine_targets_cleared_today: routine_targets_cleared_today,
            routine_remarks: routine_remarks,
            mob_duration: mob_duration,
            t_duration: t_duration,
            i_duration: i_duration,
            cs_duration: cs_duration,
            wdt_duration: wdt_duration,
            tbw_duration: tbw_duration,
            cc_duration: cc_duration,
            tdt_duration: tdt_duration,
            total_duration: total_duration,
            mob_duration_total: mob_duration_total,
            t_duration_total: t_duration_total,
            i_duration_total: i_duration_total,
            cs_duration_total: cs_duration_total,
            wdt_duration_total: wdt_duration_total,
            tbw_duration_total: tbw_duration_total,
            cc_duration_total: cc_duration_total,
            tdt_duration_total: tdt_duration_total,
            total_duration_total: total_duration_total,
            weather_interpretation: weather_interpretation,
            technical_issues: technical_issues,
            meetings: meetings,
            other_remarks: other_remarks,
            client_comments: client_comments,
            seaterra_comments: seaterra_comments
        };

        console.log(payload);

        fetch('/dprs/save-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Report saved successfully.');
            } else {
                alert('Error saving report: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error saving report:', error);
            alert('Error saving report.');
        });
    }

    function reloadTotals(date) {
        fetch('/dprs/reload-totals?date=' + encodeURIComponent(date), { method: 'GET' })
            .then(response => response.json())
            .then(data => {
            if (data.status === 'success') {
                alert('Totals reloaded. Please refresh the page.');
            } else {
                alert('Failed to reload totals.');
            }
            })
            .catch(error => {
            console.error('Error reloading totals:', error);
            alert('Error reloading totals.');
            });
    }

    function resetDPR(date) {
        if (!confirm('Are you sure you want to reset the DPR for the selected date? This action cannot be undone.')) {
            return;
        }
        fetch('/dprs/reset-dpr?date=' + encodeURIComponent(date), { method: 'GET' })
            .then(response => response.json())
            .then(data => {
            if (data.status === 'success') {
                alert('DPR reset successfully. Please refresh the page.');
            } else {
                alert('Failed to reset DPR.');
            }
            })
            .catch(error => {
            console.error('Error resetting DPR:', error);
            alert('Error resetting DPR.');
        });
    }

    function printDPR(date) {
        fetch('/dprs/print-dpr?date=' + encodeURIComponent(date), { method: 'GET' })
            .then(response => response.blob())
            .then(blob => {
            const url = URL.createObjectURL(blob);
            window.open(url);

            document.getElementById("pdfViewer").src = url;
        });
    }

    function copyDPR(){
        const popup = document.createElement('div');
        popup.style.position = 'fixed';
        popup.style.top = '0';
        popup.style.left = '0';
        popup.style.width = '100vw';
        popup.style.height = '100vh';
        popup.style.background = 'rgba(0,0,0,0.5)';
        popup.style.display = 'flex';
        popup.style.alignItems = 'center';
        popup.style.justifyContent = 'center';
        popup.style.zIndex = '10000';

        const dialog = document.createElement('div');
        dialog.style.background = '#fff';
        dialog.style.padding = '24px';
        dialog.style.borderRadius = '8px';
        dialog.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
        dialog.innerHTML = `
            <label for="copy-dpr-date">Select date to copy from:</label>
            <input type="date" id="copy-dpr-date" style="margin: 0 8px;">
            <button id="copy-dpr-confirm">Copy</button>
            <button id="copy-dpr-cancel">Cancel</button>
        `;

        popup.appendChild(dialog);
        document.body.appendChild(popup);

        document.getElementById('copy-dpr-cancel').onclick = () => {
            document.body.removeChild(popup);
        };

        document.getElementById('copy-dpr-confirm').onclick = () => {
            const sourceDate = document.getElementById('copy-dpr-date').value;
            if (!sourceDate) {
                alert('Please select a date.');
                return;
            }
            const targetDate = document.getElementById('selected-report-date').value;
            document.body.removeChild(popup);
            fetch('/dprs/copy-dpr?sourceDate=' + encodeURIComponent(sourceDate) + '&targetDate=' + encodeURIComponent(targetDate), { method: 'GET' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('DPR copied successfully. Please refresh the page.');
                    } else {
                        alert('Failed to copy DPR.');
                    }
                })
                .catch(error => {
                    console.error('Error copying DPR:', error);
                    alert('Error copying DPR.');
                });
        };
    }
});