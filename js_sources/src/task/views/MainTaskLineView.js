/*
 * File Name : MainTaskLineView.js
 *
 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
import Mn from 'backbone.marionette';
import TaskGroupCollection from '../models/TaskGroupCollection.js';
import TaskGroupModel from '../models/TaskGroupModel.js';
import TaskGroupCollectionView from './TaskGroupCollectionView.js';
import TaskGroupFormView from './TaskGroupFormView.js';
import {displayServerSuccess, displayServerError} from '../../backbone-tools.js';

const MainTaskLineView = Mn.View.extend({
    template: require('./templates/MainTaskLineView.mustache'),
    regions: {
        container: '.group-container',
        modalRegion: ".group-modalregion",
    },
    ui: {
        add_button: 'button.add'
    },
    triggers: {
        "click @ui.add_button": "group:add"
    },
    childViewEvents: {
        'group:edit': 'onGroupEdit',
        'group:delete': 'onGroupDelete',
    },
    initialize: function(options){
        this.collection = new TaskGroupCollection(options['datas']);
    },
    onDeleteSuccess: function(){
        displayServerSuccess("Vos données ont bien été supprimées");
    },
    onDeleteError: function(){
        displayServerError("Une erreur a été rencontrée lors de la " +
                           "suppression de cet élément");
    },
    onGroupDelete: function(childView){
        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cet ouvrage ?");
        if (result){
            childView.model.destroy(
                {
                    success: this.onDeleteSuccess,
                    error: this.onDeleteError
                }
            );
        }
    },
    onGroupEdit: function(childView){
        console.log("On group edit");
        this.showTaskGroupForm(childView.model, "Modifier cet ouvrage");
    },
    onGroupAdd: function(){
        var model = new TaskGroupModel({
            order: this.collection.getMaxOrder() + 1
        });
        this.showTaskGroupForm(model, "Ajouter un ouvrage");
    },
    onEditGroup: function(childView){
        var model = childView.model;
        this.showTaskGroupForm(model, "Modifier cet ouvrage");
    },
    showTaskGroupForm: function(model, title){
        var form = new TaskGroupFormView(
            {
                model: model,
                title: title,
                destCollection: this.collection
            }
        );
        console.log("Showing the form");
        console.log(this.getRegion('modalRegion'));
        this.showChildView('modalRegion', form);
    },
    onChildviewDestroyModal: function() {
        console.log("onChildviewDestroyModal");
        this.detachChildView('modalRegion');
    	this.getRegion('modalRegion').empty();
  	},
    onRender: function(){
        this.showChildView(
            'container',
            new TaskGroupCollectionView(
                {collection: this.collection}
            )
        );
    }
});
export default MainTaskLineView;
