$(document).ready(function(){
  $('#message_l').scrollTop($('#message_l')[0].scrollHeight);
  var csrf = $("input[name=csrfmiddlewaretoken]").val();
  function refresh(){
    $.ajax({
      url: '',
      type: 'get',
      data: {
        id: $('#message_l').attr('class')
      },
      success: function(response) {
        if (response.id != $('#message_l').attr('class')){
          console.log(response)
          $.each(response.name, function(i, val){
            $("#message_l").append('<strong>' + val + ' ' + '</strong>')
            $("#message_l").append('<strong>' + response.time[i] + '</strong>')
            $("#message_l").append('<p>' + response.text[i] + '</p>')
          });
          $('#message_l').scrollTop($('#message_l')[0].scrollHeight);
        };
        $('#message_l').attr('class', response.id)
      }
    });
  }
  setInterval(function() {
    refresh()
  }, 700);

  $("#btn").click(function(){
    $.ajax({
      url: '',
      type: 'post',
      data: {
        text: $("#message_t").val(),
        csrfmiddlewaretoken: csrf
      },
      success: function(){
        $("#message_t").val('')
      }
    });
  });
});
