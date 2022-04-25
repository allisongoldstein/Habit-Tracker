

$(document).ready(function(){
    $('#submit-button').click(function(){
        var name = $('#name').val();
        if(name != '') {
            $.ajax({
                url:'/add',
                method:'POST',
                data: {name:name},
                success:function(data){
                    $('#task-modal').hide();
                    location.reload();
                }
            })
        }
    })
})

$(document).ready(function(){
    $('.task').change(function() {
        var id = this['name']
        if(this.checked) {
            var checked = 'checked'
        } else {
            var checked = 'unchecked'
        }
        $.ajax({
            url:'/check',
            method:'POST',
            data: {checked:checked, id:id},
            success:function(data){
                location.reload();
            }
        })
    })
})

$(document).ready(function(){
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
})
