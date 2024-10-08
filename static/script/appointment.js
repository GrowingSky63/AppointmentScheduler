// static/script/appointment.js

$(document).ready(function() {
    $('#filter-specialization').on('change', function() {
        var specialization = $(this).val();
        if (specialization) {
            // Clear previous doctor list, date picker, and schedule list
            $('#doctor-list').empty();
            $('#date-picker').hide();
            $('#schedule-list').empty();
            // AJAX request to get doctors based on specialization
            $.ajax({
                url: '/get_doctors/',
                data: {
                    'specialization': specialization
                },
                success: function(data) {
                    // Display list of doctors
                    if (data.doctors.length > 0) {
                        var doctorListHtml = '<ul>';
                        $.each(data.doctors, function(index, doctor) {
                            doctorListHtml += '<li><a href="#" class="doctor-link" data-doctor-id="' + doctor.id + '">' + doctor.name + '</a></li>';
                        });
                        doctorListHtml += '</ul>';
                        $('#doctor-list').html(doctorListHtml);
                    } else {
                        $('#doctor-list').html('<p>Nenhum médico disponível nesta especialização.</p>');
                    }
                }
            });
        } else {
            // Clear doctor list, date picker, and schedule list
            $('#doctor-list').empty();
            $('#date-picker').hide();
            $('#schedule-list').empty();
        }
    });

    // Delegate click event for dynamically added doctor links
    $('#doctor-list').on('click', '.doctor-link', function(e) {
        e.preventDefault();
        var doctorId = $(this).data('doctor-id');
        // Store selected doctor ID for later use
        $('#doctor-list').data('selected-doctor-id', doctorId);
        // Show the date picker
        $('#date-picker').show();
        $('#selected-date').val('');
        $('#schedule-list').empty();
        // Initialize date picker
        $('#selected-date').datepicker({
            dateFormat: 'dd/mm/yy',
            minDate: 0, // Disable past dates
            onSelect: function(dateText, inst) {
                // When a date is selected, fetch available schedules
                var selectedDate = $(this).datepicker('getDate');
                var formattedDate = $.datepicker.formatDate('yy-mm-dd', selectedDate);
                var doctorId = $('#doctor-list').data('selected-doctor-id');
                // Clear previous schedule list
                $('#schedule-list').empty();
                // AJAX request to get schedules based on doctor and date
                $.ajax({
                    url: '/get_schedules/',
                    data: {
                        'doctor_id': doctorId,
                        'date': formattedDate
                    },
                    success: function(data) {
                        // Display available times
                        if (data.schedules.length > 0) {
                            var scheduleListHtml = '<ul>';
                            $.each(data.schedules, function(index, schedule) {
                                scheduleListHtml += '<li>' + schedule + ' <button class="schedule-button" data-doctor-id="' + doctorId + '" data-schedule="' + schedule + '" data-date="' + formattedDate + '">Agendar</button></li>';
                            });
                            scheduleListHtml += '</ul>';
                            $('#schedule-list').html(scheduleListHtml);
                        } else {
                            $('#schedule-list').html('<p>Nenhum horário disponível para este médico nesta data.</p>');
                        }
                    }
                });
            }
        });
    });

    // Delegate click event for dynamically added schedule buttons
    $('#schedule-list').on('click', '.schedule-button', function() {
        var doctorId = $(this).data('doctor-id');
        var schedule = $(this).data('schedule');
        var date = $(this).data('date');
        // Redirect to appointment creation page with pre-selected data
        window.location.href = '/appointment/new/?doctor_id=' + doctorId + '&schedule=' + encodeURIComponent(schedule) + '&date=' + date;
    });

});