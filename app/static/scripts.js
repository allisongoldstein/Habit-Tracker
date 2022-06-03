$(document).ready(function(){

    $('#submit-button').click(function(){
        var name = $('#name').val();
        var notes = $('#notes-content').val()
        if(name != '') {
            $.ajax({
                url:'/add',
                method:'POST',
                data: {name:name, notes:notes},
                success:function(data){
                    $('#habit-modal').hide();
                    location.reload();
                }
            })
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
        $.ajax({
            url:'/check',
            method:'POST',
            data: {checked:checked, id:id, date:date},
            success:function(data){
                location.reload();
            }
        })
    })

    $('.update-button').click(function(){
        var id = this.name
        var idRef = '#' + id
        var name = $('#habit-name', idRef).val();
        var notes = $('#notes-content', idRef).val();
        $.ajax({
            url:'/update',
            method:'POST',
            data: {id:id, name:name, notes:notes},
            success:function(data){
                location.reload();
            }
        })
    })

    $('.delete-button').click(function(){
        let confirmDelete = confirm('This will permanently delete all records of this habit. This cannot be undone.');
        if (confirmDelete) {
            var id = this.name
            $.ajax({
                url:'/delete',
                method:'POST',
                data: {id:id},
                success:function(data){
                    location.reload();
                }
            })
        } else {
            console.log('cancel delete')
        }
    })

    $('#datepicker-submit').click(function() {
        var date = $('#datepicker').val();
        $.ajax({
            success:function(data){
                window.location.href = '/viewDate/' + date
            }
        })
    })

    $('.calDate').click(function() {
        date = this.name
        moveToDate(date)
    })

})

function moveToDate(date) {
    window.location.href = '/viewDate/' + date
}

function f() {
    return
}

function editHabit(id) {
    var modal = $('#' + id)
    modal.modal()
}
