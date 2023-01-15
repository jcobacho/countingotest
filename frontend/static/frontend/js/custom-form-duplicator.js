// var form_prefix = document.currentScript.dataset.form_prefix;

/*$(document).ready(function () {

    function cloneMore(e) {
        e.preventDefault();
        const $btn = $(this);
        const container = $btn.closest(".formset_container")
        var last_row = container.find('.formset-row:last')

        const form_prefix = container.data('form_prefix')

        // // current total form count
        // var count = parseInt($('#id_form-TOTAL_FORMS').val());
        // console.log("count")
        // console.log(count)
        // // update django Total form count
        // $('#id_form-TOTAL_FORMS').val(count + 1);

        // current total form count
        var count = parseInt($('#id_' + form_prefix + '-TOTAL_FORMS').val());
        // update django Total form count
        $('#id_' + form_prefix + '-TOTAL_FORMS').val(count + 1);

        // gen template with updated prefix
        var template = $(`#empty_form-${form_prefix}-__prefix__`).html().replace(/__prefix__/g, count);

        var newElement = $(template);
        newElement.hide();

        if (last_row.length > 0) {
            newElement.insertAfter(last_row);
            newElement.slideDown(300);
        } else {
            // add as first element
            container.append(newElement)
            newElement.slideDown(300);

        }

        // // initialize select2 instance
        var select2elements = $(newElement).find('.django-select2');
        $.each(select2elements, function (i, input) {
            $(input).next('span.select2-container').remove()
            $(input).djangoSelect2();

        });

        var tags = $(newElement).find('tags.tagify');
        tags.each(function (j, input) {
            var textarea = $(input).next('textarea')
            input.remove()
            if(textarea.length > 0)
                new Tagify(textarea[0], {})
        });

        // // // initialize select2 instance
        // $.each(newElement.find('.select2me'), function (i, obj) {
        //     if (!$(obj).data("select2")) {
        //         $(obj).select2();
        //     }
        // });

    }

    function updateFormElementIndices(i, el) {

        var curIndex = $(el)
            .attr('id')
            .match(/\d+/)[0];

        // update form row id
        $(el).attr('id', $(el).attr('id').replace(curIndex, i));

        // update delete button
        $(el).find('a.remove-form-row').attr('data-form_prefix', $(el).attr('id').replace(curIndex, i));

        // update inputs
        var inputs = $(el).find('input');

        inputs.each(function (j, input) {
            $(input).attr('id', $(input).attr('id').replace(curIndex, i));
            $(input).attr('name', $(input).attr('name').replace(curIndex, i));
        });

        // select2 inputs
        var select2elements = $(el).find('.select2me');
        select2elements.each(function (j, input) {
            $(input).select2("destroy");
            $(input).attr('id', $(input).attr('id').replace(curIndex, i));
            $(input).djangoSelect2();
            $(input).select2();
        });

        var tags = $(el).find('tags.tagify');

        tags.each(function (j, input) {
            var textarea = $(input).next('textarea')
            if(textarea.length > 0){
                $(textarea).attr('id', $(textarea).attr('id').replace(curIndex, i));
                $(textarea).attr('name', $(textarea).attr('name').replace(curIndex, i));
                input.remove()
                new Tagify(textarea[0], {})
            }
        });


        // define all custom inputs may needed

    }

    function deleteForm(e) {
        e.preventDefault();
        var $btn = $(this);

        Swal.fire({
            text: "Are you sure you want to delete this item ?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, delete!",
            cancelButtonText: "No, cancel",
            customClass: {
                confirmButton: "btn fw-bold btn-danger",
                cancelButton: "btn fw-bold btn-active-light-primary"
            }
        }).then(function (result) {
            if (result.value) {
                console.log("$btn")
                console.log($btn)
                const container = $btn.closest(".formset_container");
                var form_prefix = $btn.data('form_prefix');
                console.log("prefix")
                console.log(form_prefix)
                var $delete_input = $('#id_' + form_prefix + '-DELETE');

                if ($delete_input.length > 0) {
                    $delete_input.prop('checked', true);
                    $('#' + form_prefix).slideUp(300);
                } else {
                    const formset_prefix = container.data('formset_prefix')
                    var count = parseInt($('#id_' + formset_prefix + '-TOTAL_FORMS').val());

                    console.log("count")
                    console.log(count)
                    $("#id_" + formset_prefix + "-TOTAL_FORMS").val(count - 1);
                    console.log("form_prefix")
                    console.log(form_prefix)
                    $('#' + form_prefix).slideUp(300, function () {
                        $(this).remove()
                        var forms = container.find(".formset-row");
                        $.each(forms, updateFormElementIndices);
                    });
                }
            }
        });

    }


    $(document).on("click", ".add-form-row", cloneMore);


    $(document).on("click", ".remove-form-row", deleteForm);


});*/
"use strict";
class DjangoFormDuplicator{

    constructor(template, formset_prefix){
        this.template = template;
        this.formset_prefix = formset_prefix;
        //this.init()
    }

    appendForm(newElement, lastRow, el){
        if (lastRow) {
            newElement.insertAfter($(lastRow));
        } else {
            // add as first element
            el.append(newElement)
        }
    }

    cloneMore(container) {

        // const container = $(btn).closest(".formset_container")
        const formset_prefix = container.data('formset_prefix')

        var lastRow = container.find('.formset-row:last')

        // current total form count
        var count = parseInt($('#id_' + formset_prefix + '-TOTAL_FORMS').val());
        // update django Total form count
        $('#id_' + formset_prefix + '-TOTAL_FORMS').val(count + 1);

        var template = $(this.template).html().replace(/__prefix__/g, count);
        var newElement = $(template);

        //newElement.hide();

        this.appendForm(newElement, lastRow, container.find('.formset-list'));

        // gen template with updated prefix
        this.show(newElement, lastRow);
        this.ready();

    }

    updateElementIndex(el, attr, curIndex, i){
        el.setAttribute(attr, el.getAttribute(attr).replace(curIndex, i));

    }

    updateFormElementIndexes(el, i) {

        var curIndex = el.getAttribute('id').match(/\d+/)[0];

        // update form row id
        el.setAttribute('id', el.getAttribute('id').replace(curIndex, i));
        this.updateElementIndex(el,'id', curIndex, i)
        // update delete btn
        this.updateElementIndex(el.querySelector('a.remove-form-row'),'data-form_prefix', curIndex, i)

        this.updateExtraFields(el, curIndex, i)

        /*// update inputs
        var inputs = el.querySelectorAll('input');

        inputs.forEach(function (input, j) {
            input.setAttribute('id', input.getAttribute('id').replace(curIndex, i));
            // find the file in uppy and update index

            input.setAttribute('name', input.getAttribute('name').replace(curIndex, i));
            if (input.getAttribute('type') === 'file' && input.getAttribute('data-id')) {
                const file = uppy.getFile(input.getAttribute('data-id'));
                file.data.input_id = file.data.input_id.replace(curIndex, i);
            }
        });*/
    }

    deleteForm(btn) {

        var fr = this;
        Swal.fire({
            text: "Are you sure you want to delete this item ?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, delete!",
            cancelButtonText: "No, cancel",
            customClass: {
                confirmButton: "btn fw-bold btn-danger",
                cancelButton: "btn fw-bold btn-active-light-primary"
            }
        }).then(function (result) {
            if (result.value) {

                fr.hide($(btn));
            }
        });

    }

    init() {

        var fr = this;

        $(document).on('click', `[data-formset_prefix=${fr.formset_prefix}] .add-form-row`, function (e) {

            e.preventDefault();
            var btn = this;
            const container = $(btn).closest(".formset_container");
            fr.cloneMore(container)
        });

        $(document).on('click', `[data-formset_prefix=${fr.formset_prefix}] .remove-form-row`, function (e) {

            e.preventDefault();
            var btn = this;
            fr.deleteForm(btn)
        });

    }

    show(newElement) {
        newElement.slideDown(300);

        // // initialize select2 instance
        var select2elements = $(newElement).find('.django-select2');
        $.each(select2elements, function (i, input) {
            $(input).next('span.select2-container').remove()
            $(input).select2();
        });

        var tags = $(newElement).find('tags.tagify');
        tags.each(function (j, input) {
            var textarea = $(input).next('textarea')
            input.remove()
            if(textarea.length > 0)
                new Tagify(textarea[0], {})
        });

    }
    hide(btn) {

        const container = btn.closest(".formset_container");
        var form_prefix = btn.data('form_prefix');
        var deleteInput = $('#id_' + form_prefix + '-DELETE');
        var deleteElement = $('#' + form_prefix)
        var fr = this;

        if (deleteInput.length > 0) {
            deleteInput.prop('checked', true);
            deleteElement.slideUp(300);
            fr.ready();
        } else {
            const formset_prefix = container.data('formset_prefix')
            var count = parseInt($('#id_' + formset_prefix + '-TOTAL_FORMS').val());
            $("#id_" + formset_prefix + "-TOTAL_FORMS").val(count - 1);
            deleteElement.slideUp(300, function () {
                $(this).remove()

                var forms = container[0].querySelectorAll(".formset-row");
                forms.forEach(function (el, i) {
                    fr.updateFormElementIndexes(el, i)
                });
                fr.ready();
            });

        }
    }

    updateExtraFields(formsetRow, curIndex, i){

        // update inputs
        var inputs = formsetRow.querySelectorAll('input');
        var uei = this.updateElementIndex;
        inputs.forEach(function(input, j){

            uei(input,'id', curIndex, i)
            uei(input,'name', curIndex, i)

        })
        var fr = this

       /* inputs.each(function (j, input) {
            if(input.hasAttribute('id'))
                $(input).attr('id', $(input).attr('id').replace(curIndex, i));
            if($(input).hasAttribute('name'))
                $(input).attr('name', $(input).attr('name').replace(curIndex, i));
        });*/

        // select2 inputs
        var select2elements = formsetRow.querySelectorAll('select.django-select2');
        select2elements.forEach(function(input, j){
            fr.updateElementIndex(input,'id', curIndex, i);
            fr.updateElementIndex(input,'name', curIndex, i)
            $(input).next('span.select2-container').remove()
            $(input).select2();
        });

        var tags = formsetRow.querySelectorAll('tags.tagify');

        tags.forEach(function(input, j){
            var $textarea = $(input).next('textarea')

            if($textarea.length > 0){
                var textarea = $textarea[0];
                fr.updateElementIndex(textarea,'id', curIndex, i);
                fr.updateElementIndex(textarea, 'name', curIndex, i);

                input.remove()
                new Tagify(textarea, {})
            }
        });

    }
    ready(){
        // any additional usage after form has been duplicated or updated
    }


    // Public methods

};