$(document).ready(function(){

    $('#submit-button').click(function(){
        var name = $('#name').val();
        if(name != '') {
            $.ajax({
                url:'/add',
                method:'POST',
                data: {name:name},
                success:function(data){
                    $('#habit-modal').hide();
                    location.reload();
                }
            })
        }
    })

    $('#custom-schedule').change(function(){
        if (this.checked) {
            console.log('custom schedule')
        } else {
            console.log('no custom schedule')
        }
    })

    $('.habit').change(function() {
        var id = this['name']
        if(this.checked) {
            var checked = 'checked'
        } else {
            var checked = 'unchecked'
        }
        var date = $('#viewDate').text()
        console.log(date)
        $.ajax({
            url:'/check',
            method:'POST',
            data: {checked:checked, id:id, date:date},
            success:function(data){
                location.reload();
            }
        })
    })

    $('.delete-button').click(function(){
        var id = this.name
        $.ajax({
            url:'/delete',
            method:'POST',
            data: {id:id},
            success:function(data){
                location.reload();
            }
        })
    })

    $('#datepicker-submit').click(function() {
        var date = $('#datepicker').val();
        console.log(date)
        $.ajax({
            success:function(data){
                window.location.href = '/viewDate/' + date
            }
        })
    })

    $('.calDate').click(function() {
        date = this.name
        console.log(date)
        moveToDate(date)
    })

})

function moveToDate(date) {
    window.location.href = '/viewDate/' + date
}

function f() {
    return
}
