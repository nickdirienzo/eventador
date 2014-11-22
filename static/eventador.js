$(document).ready(function() {

  $("#calendar").fullCalendar({
    eventSources: [{
      url: '/events',
      ignoreTimezone: false
    }]
  });

  $("#search-box").submit(function(e) {
    e.preventDefault();
    $.get("/" + $("#domain").val() + "/search?query=" + $("#query").val(), function(data) {
      $("#results").html("");
      if(data.emails.length == 0) {
        $("#results").html("No results for: \"" + $("#query").val() + "\"");
      } else {
        for(i in data.emails) {
          email = data.emails[i];
          $("#results").append("<p>" + email.subject + "</p>");
        }
      }
    });
  });

});
