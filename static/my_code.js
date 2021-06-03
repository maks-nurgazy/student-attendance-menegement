(function ($) {
    $(function () {
        let department = $('#id_department');
        let st_class_div = $('.field-st_class');
        let st_class = $('.id_st_class');
        st_class_div.hide();
        department.change(function () {
            let d = department.val();
            if (d) {
                $.get(`http://127.0.0.1:8000/attendance-management/api/departments/${d}/classes/`, function (data, status) {

                    let str = data.classes.map(e => (
                        `<option value="${e.id}">${e.num} course</option>`
                    ));
                    console.log(str);
                    st_class_div.show();
                });
            } else {
                st_class_div.hide();
            }


        });
    });
})(django.jQuery);
