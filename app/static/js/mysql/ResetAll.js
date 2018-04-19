$(".reset_btn").click(function(){
    $(".list_area").val("is-empty");
    $(".text_area").val("");
    $(".review_area").addClass('hidden');
    $(".commit_btn").addClass('hidden');
    $(".review_btn").removeClass('hidden');
    $(".backup_check").prop('checked',true);
});