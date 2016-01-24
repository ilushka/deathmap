$(document).ready(function () {
  // Update button:
  $("#update-user-btn").click(function (event) {
    event.preventDefault();
    var user = {};

    user.first = $("input[name='firstname']").val();
    user.last = $("input[name='lastname']").val();
    user.twitter = $("input[name='twitter']").val();
    user.oldpassword = $("input[name='old-password']").val();
    user.newpassword = $("input[name='new-password']").val();

    $.ajax({
      type: "POST",
      url: window.location.pathname,
      data: JSON.stringify(user),
      dataType: "json",
      contentType: "application/json",
      success: function() {
        alert("Sent user data");
      },
      error: function(jqXHR, textStatus, errorThrown) {
        alert("Failed to send user data " + textStatus + " " + errorThrown);
      }
    });
  });
});

