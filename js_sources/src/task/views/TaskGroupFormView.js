/*
 * File Name : TaskGroupFormView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import InputWidget from './InputWidget.js';
import TextAreaWidget from './TextAreaWidget.js';
import ModalFormBehavior from '../behaviors/ModalFormBehavior.js';
var template = require('./templates/TaskGroupFormView.mustache');

const TaskGroupFormView = Mn.View.extend({
    template: template,
    regions: {
        'title': '.title',
        'description': '.description',
    },
    ui: {
        btn_cancel: "button[type=reset]",
        form: "form",
        submit: 'button[type=submit]',
    },
    behaviors: [ModalFormBehavior],
    triggers: {
        'click @ui.btn_cancel': 'close:modal'
    },
    childViewEvents: {
        'change': 'onChildChange'
    },
    onChildChange: function(attribute, value){
        this.triggerMethod('data:modified', this, attribute, value);
    },
    templateContext: function(){
        return {
            title: this.getOption('title')
        };
    },
    onRender: function(){
        this.showChildView(
            'title',
            new InputWidget(
                {
                    value: this.model.get('title'),
                    title: "Titre (optionnel)",
                    description: "Titre de l'ouvrage tel qu'affiché dans la sortie pdf, laissez vide pour ne pas le faire apparaître",
                    field_name: "title"
                }
            )
        );
        this.showChildView(
            'description',
            new TextAreaWidget({
                value: this.model.get('description'),
                title: "Description (optionnel)",
                field_name: "description",
                tinymce: true,
                cid: this.model.cid
            })
        );
    }
});
export default TaskGroupFormView;
