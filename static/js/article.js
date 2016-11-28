$(document).ready(function () {
  // setup article delete button function
  $(":button").click(function() {
    var id = $(this).attr("article"),
        row = $(this).parent().parent();
    $.post("/article/" + id + "/", function() {
      row.remove();
    })
    .fail(function() {
      alert("Failed to delete article " + id);
    });
  });
});

