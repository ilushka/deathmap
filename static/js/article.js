$(document).ready(function () {
  // setup article delete button function
  $(".del-article-btn:button").click(function() {
    var id = $(this).attr("article"),
        row = $(this).parent().parent();
    $.post("/article/" + id + "/", function() {
      row.remove();
    })
    .fail(function() {
      alert("Failed to delete article " + id);
    });
  });

  // job polling
  var poll_job = function(key) {
    $.get("/job/" + key + "/", function(data) {
      alert("MONKEY: " + data);
    })
    .fail(function() {
      alert("Failed to get job status " + key);
    });
  };

  // setup article body load function
  $("#article_modal").on("shown.bs.modal", function() {
    var id = $(this).attr("article");
    $.get("/article/" + id + "/", function(data) {
      var json = $.parseJSON(data);
      poll_job(json['job_key']);
    })
    .fail(function() {
      alert("Failed to load article " + id);
    });
  });
});

