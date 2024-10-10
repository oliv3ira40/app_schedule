$(function() {
    var my_appointments = $('.my-appointments');
    
    if (my_appointments.length) {
        var input_cpf = my_appointments.find('#cpf');
        input_cpf.mask('000.000.000-00', {reverse: true});
        
        var input_phone = my_appointments.find('#phone');
        input_phone.mask('00 00000-0000', {reverse: true});
    }
})
