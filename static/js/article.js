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
  var poll_job = function(key, completion) {
    $.get("/job/" + key + "/", function(json) {
      if (json["status"] == "is_finished") {
        completion(json);
      } else {
        setTimeout(function() { poll_job(key, completion); }, 2000);
      }
    })
    .fail(function() {
      alert("Failed to get job status " + key);
    });
  };

  // load article
  var load_article = function(id, completion) {
    $.get("/article/" + id + "/", function(json) {
      poll_job(json["job_key"], completion);
    })
    .fail(function() {
      alert("Failed to load article " + id);
    });
  };

  // setup article load button function
  $(".load-article-btn:button").click(function() {
    var id = $(this).data("article");
    load_article(id, function(body) {
      $("#article-modal-body").text(body);
      $("#article-modal").modal();
    });
  });
});

