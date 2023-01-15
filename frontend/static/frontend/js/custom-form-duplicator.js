
class DjangoFormDuplicator{

    constructor(template, formset_prefix){
        this.template = template;
        this.formset_prefix = formset_prefix;
        //this.init()
    }

    appendForm(newElement, lastRow, el){
        if (lastRow.length > 0) {
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
        var select2elements = $(newElement).find('.select2-hidden-accessible');
        $.each(select2elements, function (i, input) {
            $(input).next('span.select2-container').remove()
            $(input).select2();
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

        // select2 inputs
        var select2elements = formsetRow.querySelectorAll('select2-hidden-accessible');
        select2elements.forEach(function(input, j){
            fr.updateElementIndex(input,'id', curIndex, i);
            fr.updateElementIndex(input,'name', curIndex, i)
            $(input).next('span.select2-container').remove()
            $(input).select2();
        });
    }
    ready(){
        // any additional usage after form has been duplicated or updated
    }


    // Public methods

};