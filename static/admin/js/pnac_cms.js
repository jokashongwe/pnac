(function () {
    function refreshEditors() {
        if (!window.editors) {
            return;
        }
        Object.keys(window.editors).forEach(function (key) {
            var editor = window.editors[key];
            if (editor && editor.ui && typeof editor.ui.update === "function") {
                editor.ui.update();
            }
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        document.body.addEventListener("shown.bs.tab", refreshEditors);
        document.body.addEventListener("shown.bs.collapse", refreshEditors);
        document.querySelectorAll('a[data-toggle="tab"], a[data-toggle="pill"]').forEach(function (el) {
            el.addEventListener("shown.bs.tab", refreshEditors);
        });
        window.setTimeout(refreshEditors, 400);
    });
})();
