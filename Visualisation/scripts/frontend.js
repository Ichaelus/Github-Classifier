console.log("Frontend started..");

$.ajax({
  type: "GET",
  url: "../post/test",
}).done(function(res) {
   alert(res);
});