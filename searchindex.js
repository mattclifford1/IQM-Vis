Search.setIndex({docnames:["IQM_Vis","IQM_Vis.UI","IQM_Vis.data_handlers","IQM_Vis.examples","IQM_Vis.examples.images","IQM_Vis.metrics","IQM_Vis.metrics.NLPD_torch","IQM_Vis.metrics.NLPD_torch.layers","IQM_Vis.metrics.NLPD_torch.utils","IQM_Vis.transformations","IQM_Vis.utils","Tutorials","about","getting_started","index","modules","notebooks/Tutorial_1-making_the_UI","notebooks/Tutorial_2-Customisation","notebooks/Tutorial_3-running_an_experiment","what-are-IQMs"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":5,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.viewcode":1,nbsphinx:4,sphinx:56},filenames:["IQM_Vis.rst","IQM_Vis.UI.rst","IQM_Vis.data_handlers.rst","IQM_Vis.examples.rst","IQM_Vis.examples.images.rst","IQM_Vis.metrics.rst","IQM_Vis.metrics.NLPD_torch.rst","IQM_Vis.metrics.NLPD_torch.layers.rst","IQM_Vis.metrics.NLPD_torch.utils.rst","IQM_Vis.transformations.rst","IQM_Vis.utils.rst","Tutorials.rst","about.rst","getting_started.rst","index.rst","modules.rst","notebooks/Tutorial_1-making_the_UI.ipynb","notebooks/Tutorial_2-Customisation.ipynb","notebooks/Tutorial_3-running_an_experiment.ipynb","what-are-IQMs.rst"],objects:{"":[[0,0,0,"-","IQM_Vis"]],"IQM_Vis.UI":[[1,0,0,"-","custom_widgets"],[1,0,0,"-","experiment_mode"],[1,0,0,"-","images"],[1,0,0,"-","layout"],[1,0,0,"-","main"],[1,0,0,"-","threads"],[1,0,0,"-","utils"],[1,0,0,"-","widgets"]],"IQM_Vis.UI.custom_widgets":[[1,1,1,"","ClickLabel"],[1,1,1,"","ProgressBar"]],"IQM_Vis.UI.custom_widgets.ClickLabel":[[1,2,1,"","clicked"],[1,3,1,"","mousePressEvent"]],"IQM_Vis.UI.experiment_mode":[[1,1,1,"","make_experiment"],[1,4,1,"","make_name_for_trans"],[1,4,1,"","sort_list"]],"IQM_Vis.UI.experiment_mode.make_experiment":[[1,3,1,"","change_experiment_images"],[1,3,1,"","clicked_image"],[1,3,1,"","closeEvent"],[1,3,1,"","experiment_layout"],[1,3,1,"","finish_experiment"],[1,3,1,"","get_all_images"],[1,3,1,"","get_single_transform_im"],[1,3,1,"","init_style"],[1,3,1,"","partition"],[1,3,1,"","quick_sort"],[1,3,1,"","quit"],[1,3,1,"","reset_experiment"],[1,3,1,"","save_experiment"],[1,2,1,"","saved_experiment"],[1,3,1,"","setup_experiment"],[1,3,1,"","show_all_images"],[1,3,1,"","start_experiment"],[1,3,1,"","swap_inds"],[1,3,1,"","toggle_experiment"]],"IQM_Vis.UI.images":[[1,1,1,"","images"]],"IQM_Vis.UI.images.images":[[1,3,1,"","change_data"],[1,3,1,"","change_metric_correlations_graph"],[1,3,1,"","change_metric_range_graph"],[1,3,1,"","change_to_specific_trans"],[1,3,1,"","completed_range_results"],[1,3,1,"","display_images"],[1,3,1,"","display_metric_correlation_plot"],[1,3,1,"","display_metric_images"],[1,3,1,"","display_metric_range_plot"],[1,3,1,"","display_metrics"],[1,3,1,"","display_metrics_graph"],[1,3,1,"","display_metrics_text"],[1,3,1,"","display_radar_plots"],[1,3,1,"","get_metrics_over_all_trans_with_init_values"],[1,3,1,"","init_worker_thread"],[1,3,1,"","load_human_experiment"],[1,3,1,"","load_new_images_folder"],[1,3,1,"","plot_radar_graph"],[1,3,1,"","redo_plots"],[1,2,1,"","request_range_work"],[1,3,1,"","stopped_range_results"],[1,2,1,"","view_correlation_instance"]],"IQM_Vis.UI.layout":[[1,1,1,"","layout"]],"IQM_Vis.UI.layout.layout":[[1,3,1,"","init_layout"],[1,3,1,"","init_style"]],"IQM_Vis.UI.main":[[1,1,1,"","make_app"],[1,4,1,"","set_checked_menu_from_iterable"]],"IQM_Vis.UI.main.make_app":[[1,3,1,"","change_save_folder"],[1,3,1,"","closeEvent"],[1,3,1,"","construct_UI"],[1,3,1,"","get_menu_checkboxes"],[1,3,1,"","make_menu"],[1,3,1,"","make_status_bar"],[1,3,1,"","quit"],[1,3,1,"","reset_correlation_data"]],"IQM_Vis.UI.threads":[[1,1,1,"","get_range_results_worker"]],"IQM_Vis.UI.threads.get_range_results_worker":[[1,2,1,"","completed"],[1,2,1,"","current_image"],[1,3,1,"","do_work"],[1,2,1,"","progress"],[1,3,1,"","stop"],[1,2,1,"","stopped"]],"IQM_Vis.UI.utils":[[1,4,1,"","add_layout_to_tab"]],"IQM_Vis.UI.widgets":[[1,1,1,"","widgets"]],"IQM_Vis.UI.widgets.widgets":[[1,3,1,"","change_display_im_display_brightness"],[1,3,1,"","change_display_im_rgb_brightness"],[1,3,1,"","change_display_im_size"],[1,3,1,"","change_graph_size"],[1,3,1,"","change_human_scores_after_exp"],[1,3,1,"","change_num_steps"],[1,3,1,"","change_plot_lims"],[1,3,1,"","change_post_processing"],[1,3,1,"","change_pre_processing"],[1,3,1,"","display_slider_num"],[1,3,1,"","generic_value_change"],[1,3,1,"","init_widgets"],[1,3,1,"","launch_experiment"],[1,3,1,"","reset_slider_group"],[1,3,1,"","reset_sliders"],[1,3,1,"","set_image_name_text"],[1,3,1,"","update_image_settings"],[1,3,1,"","update_progress"],[1,3,1,"","update_status_bar"]],"IQM_Vis.data_handlers":[[2,0,0,"-","data_api"],[2,0,0,"-","data_api_abstract"]],"IQM_Vis.data_handlers.data_api":[[2,1,1,"","dataset_holder"]],"IQM_Vis.data_handlers.data_api.dataset_holder":[[2,3,1,"","get_image_to_transform"],[2,3,1,"","get_image_to_transform_name"],[2,3,1,"","get_metric_images"],[2,3,1,"","get_metrics"],[2,3,1,"","get_reference_image"],[2,3,1,"","get_reference_image_name"],[2,3,1,"","load_image_list"]],"IQM_Vis.data_handlers.data_api_abstract":[[2,1,1,"","base_dataloader"],[2,1,1,"","base_dataset_loader"]],"IQM_Vis.data_handlers.data_api_abstract.base_dataloader":[[2,3,1,"","get_image_to_transform"],[2,3,1,"","get_image_to_transform_name"],[2,3,1,"","get_metric_images"],[2,3,1,"","get_metrics"],[2,3,1,"","get_reference_image"],[2,3,1,"","get_reference_image_name"],[2,5,1,"","metric_images"],[2,5,1,"","metrics"]],"IQM_Vis.examples":[[3,0,0,"-","all"],[3,0,0,"-","dataset"],[3,0,0,"-","dists"],[3,0,0,"-","experiment"],[4,0,0,"-","images"],[3,0,0,"-","kodak"],[3,0,0,"-","multiple"],[3,0,0,"-","simple"]],"IQM_Vis.examples.all":[[3,4,1,"","run"]],"IQM_Vis.examples.dataset":[[3,4,1,"","run"]],"IQM_Vis.examples.dists":[[3,4,1,"","correct"],[3,4,1,"","load_and_calibrate_image"],[3,4,1,"","run"]],"IQM_Vis.examples.experiment":[[3,4,1,"","run"]],"IQM_Vis.examples.kodak":[[3,4,1,"","run"]],"IQM_Vis.examples.multiple":[[3,4,1,"","run"]],"IQM_Vis.examples.simple":[[3,4,1,"","run"]],"IQM_Vis.metrics":[[5,0,0,"-","IQMs"],[6,0,0,"-","NLPD_torch"],[5,4,1,"","get_all_IQM_params"],[5,4,1,"","get_all_metric_images"],[5,4,1,"","get_all_metrics"]],"IQM_Vis.metrics.IQMs":[[5,1,1,"","DISTS"],[5,1,1,"","LPIPS"],[5,1,1,"","MAE"],[5,1,1,"","MSE"],[5,1,1,"","MS_SSIM"],[5,1,1,"","NLPD"],[5,1,1,"","SSIM"],[5,1,1,"","one_over_PSNR"]],"IQM_Vis.metrics.IQMs.DISTS":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.LPIPS":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.MAE":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.MSE":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.MS_SSIM":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.NLPD":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.SSIM":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.one_over_PSNR":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.NLPD_torch":[[7,0,0,"-","layers"],[6,0,0,"-","pyramids"],[8,0,0,"-","utils"]],"IQM_Vis.metrics.NLPD_torch.layers":[[7,0,0,"-","divisive_normalisation"]],"IQM_Vis.metrics.NLPD_torch.layers.divisive_normalisation":[[7,1,1,"","GDN"]],"IQM_Vis.metrics.NLPD_torch.layers.divisive_normalisation.GDN":[[7,2,1,"","beta"],[7,2,1,"","beta_reparam"],[7,3,1,"","clamp_parameters"],[7,3,1,"","forward"],[7,2,1,"","gamma"],[7,2,1,"","groups"],[7,2,1,"","reparam_offset"],[7,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.pyramids":[[6,1,1,"","LaplacianPyramid"],[6,1,1,"","LaplacianPyramidGDN"],[6,1,1,"","SteerablePyramid"],[6,1,1,"","SteerableWavelet"]],"IQM_Vis.metrics.NLPD_torch.pyramids.LaplacianPyramid":[[6,3,1,"","DN_filters"],[6,3,1,"","forward"],[6,3,1,"","pyramid"],[6,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.pyramids.LaplacianPyramidGDN":[[6,3,1,"","compare"],[6,3,1,"","pyramid"],[6,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.pyramids.SteerablePyramid":[[6,2,1,"","TODO"],[6,3,1,"","forward"],[6,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.pyramids.SteerableWavelet":[[6,2,1,"","Xcosn"],[6,2,1,"","Xrcos"],[6,2,1,"","YIrcos"],[6,2,1,"","Ycosn"],[6,2,1,"","Yrcos"],[6,2,1,"","angles"],[6,2,1,"","const"],[6,3,1,"","forward"],[6,2,1,"","harmincs"],[6,3,1,"","meshgrid_angle"],[6,2,1,"","num_orientations"],[6,2,1,"","steer_matrix"],[6,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.utils":[[8,0,0,"-","conv"],[8,0,0,"-","pyramid_filters"]],"IQM_Vis.metrics.NLPD_torch.utils.conv":[[8,4,1,"","pad"]],"IQM_Vis.transformations":[[9,4,1,"","get_all_transforms"],[9,0,0,"-","transforms"]],"IQM_Vis.transformations.transforms":[[9,4,1,"","binary_threshold"],[9,4,1,"","blur"],[9,4,1,"","brightness"],[9,4,1,"","brightness_hsv"],[9,4,1,"","contrast"],[9,4,1,"","hue"],[9,4,1,"","jpeg_compression"],[9,4,1,"","rotation"],[9,4,1,"","salt_and_pepper_noise"],[9,4,1,"","saturation"],[9,4,1,"","x_shift"],[9,4,1,"","y_shift"],[9,4,1,"","zoom_image"]],"IQM_Vis.ui_wrapper":[[0,1,1,"","make_UI"],[0,4,1,"","test_datastore_attributes"]],"IQM_Vis.ui_wrapper.make_UI":[[0,3,1,"","show"]],"IQM_Vis.utils":[[10,0,0,"-","gui_utils"],[10,0,0,"-","image_utils"],[10,0,0,"-","plot_utils"],[10,0,0,"-","save_utils"]],"IQM_Vis.utils.gui_utils":[[10,1,1,"","MplCanvas"],[10,4,1,"","change_im"],[10,4,1,"","get_image_pair_name"],[10,4,1,"","get_metric_image_name"],[10,4,1,"","get_trans_dict_from_str"],[10,4,1,"","get_transformed_image_name"],[10,4,1,"","str_to_len"]],"IQM_Vis.utils.image_utils":[[10,4,1,"","calibrate_brightness"],[10,4,1,"","crop_centre"],[10,4,1,"","get_transform_image"],[10,4,1,"","load_image"],[10,4,1,"","resize_image"],[10,4,1,"","resize_to_longest_side"],[10,4,1,"","save_image"]],"IQM_Vis.utils.plot_utils":[[10,1,1,"","bar_plotter"],[10,4,1,"","click_scatter"],[10,4,1,"","compute_metric_for_human_correlation"],[10,4,1,"","compute_metrics_over_range"],[10,4,1,"","compute_metrics_over_range_single_trans"],[10,4,1,"","get_all_single_transform_params"],[10,4,1,"","get_all_slider_values"],[10,4,1,"","get_correlation_plot"],[10,4,1,"","get_radar_plots_avg_plots"],[10,4,1,"","get_transform_range_plots"],[10,4,1,"","hover_scatter"],[10,1,1,"","line_plotter"],[10,1,1,"","radar_plotter"],[10,1,1,"","scatter_plotter"],[10,4,1,"","update_annot"]],"IQM_Vis.utils.plot_utils.bar_plotter":[[10,3,1,"","plot"],[10,3,1,"","set_plot_lims"],[10,3,1,"","set_style"],[10,3,1,"","show"]],"IQM_Vis.utils.plot_utils.line_plotter":[[10,3,1,"","plot"],[10,3,1,"","set_plot_lims"],[10,3,1,"","set_style"],[10,3,1,"","show"]],"IQM_Vis.utils.plot_utils.radar_plotter":[[10,3,1,"","plot"],[10,3,1,"","set_plot_lims"],[10,3,1,"","set_style"],[10,3,1,"","show"]],"IQM_Vis.utils.plot_utils.scatter_plotter":[[10,3,1,"","plot"],[10,3,1,"","set_plot_lims"],[10,3,1,"","set_style"],[10,3,1,"","show"]],"IQM_Vis.utils.save_utils":[[10,4,1,"","load_json_dict"],[10,4,1,"","load_obj"],[10,4,1,"","save_experiment_results"],[10,4,1,"","save_json_dict"],[10,4,1,"","save_obj"]],IQM_Vis:[[1,0,0,"-","UI"],[2,0,0,"-","data_handlers"],[3,0,0,"-","examples"],[5,0,0,"-","metrics"],[9,0,0,"-","transformations"],[0,0,0,"-","ui_wrapper"],[10,0,0,"-","utils"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","function","Python function"],"5":["py","property","Python property"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:function","5":"py:property"},terms:{"0":[5,7,9,10,16,17],"01":5,"03":5,"06":7,"06281v4":7,"1":[1,5,6,7,9,10,14,17],"100":[9,10,17],"101":9,"11":[5,10],"128":10,"150":1,"1511":7,"18":7,"180":17,"1995":6,"1e":7,"2":[6,7,9,10,14],"200":3,"2015":7,"2016_hvei":5,"250":10,"255":9,"256":3,"2x":[9,10],"3":[6,7,10,13,14,17],"39":17,"4":[6,17],"41":17,"5":[1,5,9,10,16,17],"6":[1,7,17],"7":9,"814697265625e":7,"9":13,"90":9,"abstract":2,"ball\u00e9":7,"boolean":[6,7],"class":[0,1,2,5,6,7,10],"const":6,"default":[2,5,6,7,9,10,16],"do":[10,12,13,14,16],"float":[6,7,9,10,17],"function":[1,2,6,7,8,10,16,17,19],"import":[13,16,17,19],"int":[6,7,8,9,17],"new":[1,13,16],"return":[5,6,7,8,9,10,17,18],"true":[0,1,3,5,6,7,10,17],"try":13,"while":6,A:[6,7],For:[2,17],If:[2,6,7,13,18],In:[7,16,17,18,19],It:[5,12,13,19],On:18,The:[5,6,7,8,12,16,18,19],Then:[6,13],There:[13,19],These:[14,17,19],To:[16,17,18],_:8,__call__:5,__init__:6,_plot:10,_redo_plot:1,_variablefunctionsclass:6,a0:1,a_tran:1,ab:7,abc:2,abl:14,about:1,absolut:5,acceler:12,access:[0,12],accord:19,achiev:12,across:10,act:7,action_stor:1,activ:[7,13],ad:[12,17],add:[1,9,16],add_layout_to_tab:1,adher:19,adjust:[9,16],advantag:12,after:[2,10,16],afterward:6,against:[12,18],aim:19,al:[5,7],alex:5,algorithm:[12,18,19],align:5,all:[0,1,2,5,6,8,9,10,15,16,18],also:[7,12,13,17,19],although:6,alwai:7,amount:[6,8,9],an:[1,2,5,6,7,9,12,16,17],anaconda:13,analys:[12,14],analysi:[12,17],angl:[6,9],angular:6,ani:[12,14,16],annot:10,api:[0,2],app:1,append_char:10,appli:[1,2,7,16,19],apply_independ:7,approach:7,apt:13,ar:[0,1,2,5,6,7,8,9,12,13,14,18,19],arbitrari:5,architectur:6,area:9,arg:1,argument:5,around:[9,13],arrai:[1,5,9,10],arxiv:7,aspect:17,associ:5,assum:8,attempt:19,attribut:0,automat:12,avaiabl:3,avail:5,avoid:7,ax:10,b:[9,16,18],b_tran:1,backend:[5,10,12],backend_qtagg:10,backpropog:7,balle2015gdn:7,band:6,bar:16,bar_nam:10,bar_plott:10,base:[0,1,2,5,6,7,10],base_dataload:2,base_dataset_load:2,basic:17,batch:5,batch_siz:7,been:6,befor:[16,17],behav:14,behaviour:19,being:[8,10,19],benchmark:19,best:[10,19],beta:7,beta_min:7,beta_reparam:7,better:9,between:[1,5,19],beyond:9,bia:7,binari:9,binary_threshold:9,black:[9,16],blank:16,blueprint:2,blur:[9,17],boarder:16,bool:[0,5,6,7,10],both:[2,19],box:12,bright:[9,17],brightness_hsv:9,bundl:17,button:[1,18],calc_rang:1,calcul:[1,8,12,16],calibr:[12,18],calibrate_bright:10,call:[5,6,7,16],callabl:2,can:[1,7,12,13,14,16,17,18,19],candela:16,capabilit:12,captur:19,care:6,carefulli:7,categoris:19,centr:[9,10],chang:[1,10,13,16,17],change_data:1,change_display_im_display_bright:1,change_display_im_rgb_bright:1,change_display_im_s:1,change_experiment_imag:1,change_graph_s:1,change_human_scores_after_exp:1,change_im:10,change_metric_correlations_graph:1,change_metric_range_graph:1,change_num_step:1,change_plot_lim:1,change_post_process:1,change_pre_process:1,change_save_fold:1,change_to_specific_tran:1,change_trans_value_sign:10,channel:7,checked_transform:1,choos:5,chosen:7,clamp:7,clamp_paramet:7,clash:13,click:[1,10,16,18],click_scatt:10,clickabl:1,clicked_imag:1,clicklabel:1,clip:9,close:7,closeev:1,co:6,code:[5,10,13],collect:12,com:[5,16,17,18],commun:2,comp:17,compar:[6,12,17,18,19],comparison:[5,12],complet:1,completed_range_result:1,comprehens:14,compress:9,comput:[6,10,16],compute_metric_for_human_correl:10,compute_metrics_over_rang:10,compute_metrics_over_range_single_tran:10,conda:13,conduct:[12,14],conf:6,conform:[12,14],connect_func:1,consist:19,construct_ui:1,constructor:2,contain:[6,8,10,16,18],content:15,context:19,contrast:9,control:5,conv:[5,6],conveni:12,conver:9,convert:9,convoltuion:7,convolut:[7,8,9],copi:16,correct:[0,3,12,18],correl:[10,12,18,19],correspond:[10,16,18],could:13,cover:12,creat:[1,13,19],crop:[2,10,12,16],crop_centr:10,crope:10,crucial:12,css_file:1,csv:18,current:10,current_imag:1,cursor0:13,custom:[1,12,17],custom_widget:[0,15],customis:[14,18],data:[0,1,2,10,12,14,17,19],data_api:[0,10,15],data_api_abstract:[0,15],data_handl:[0,15],data_stor:[0,1,10],dataset:[0,1,10,12,13,15],dataset_hold:[2,17],datastor:17,dc:6,debug:0,decod:9,decreas:9,deep:[5,19],default_save_dir:[0,1],defin:[6,17],degre:9,demonstr:13,densiti:7,depend:13,deriv:6,design:12,desir:[12,17],despit:19,detail:[12,14],determin:7,develop:12,dfferent:6,dict:[0,1,2,10],dict_:10,dictionari:[2,17],differ:[2,6,13,14],digit:9,dim:6,dimens:[5,6],dingkeyan93:5,directori:16,disagre:18,disp_len:1,displai:[12,18],display_bright:[1,10],display_imag:1,display_metr:1,display_metric_correlation_plot:1,display_metric_imag:1,display_metric_range_plot:1,display_metrics_graph:1,display_metrics_text:1,display_radar_plot:1,display_slider_num:1,dissimilar:5,dist:[0,5,15],distanc:19,distor:14,distort:[12,14,17,19],divid:7,divis:7,divisive_normalis:[5,6],divisv:7,dn_filter:6,do_work:1,doc:[0,10,16,17,18],document:[12,17],domain:[6,8],done:6,down:1,downsampl:6,dpi:10,drop:1,dtype:[6,7],e:[5,6,13,14,16,19],each:[6,7,10],earli:5,effect:14,element:[1,6],empir:19,en:5,enabl:12,encod:9,entri:[1,6],environ:13,equal:7,error:[5,13,19],es:5,et:[5,7],etc:[0,18],euclidean:19,ev:1,evalu:[5,12,14,19],event:[1,10],everi:6,everyth:[17,18],exampl:[0,2,5,13,15,17,19],exeprt:8,expect:14,expens:19,experi:[0,1,10,14,15,19],experiment:19,experiment_layout:1,experiment_mod:[0,15],expert:[6,7,8],expos:12,extent:1,extra:13,extrem:19,f:17,facilit:[12,14],fail:12,fals:[0,1,5,6,7,10],featur:12,feel:17,figur:10,figurecanvasqtagg:10,file:[2,3,10,16,17,18],filepath:17,fill:9,filt:6,filt_siz:8,filter:[6,8],finish_experi:1,first:[6,13,17,18,19],firstli:14,fix:10,flexibl:6,float32:9,folder:[1,16,18],form:12,former:6,forward:[6,7],fourier:[5,6],frame:10,framework:12,free:17,freeman:6,fresh:13,from:[1,2,5,6,8,10,12,13,16,18,19],further:[12,14],g:[5,13,14,16],gain:5,gamma:7,gamma_init:7,gan:5,gather:19,gaussian:9,gdn:7,gener:[2,5,7,12,18],generalis:7,generic_value_chang:1,geometr:5,get:[0,5,7,9,10,17],get_all_imag:1,get_all_iqm_param:5,get_all_metr:5,get_all_metric_imag:5,get_all_single_transform_param:10,get_all_slider_valu:10,get_all_transform:9,get_correlation_plot:10,get_image_pair_nam:10,get_image_to_transform:2,get_image_to_transform_nam:2,get_menu_checkbox:1,get_metr:2,get_metric_imag:2,get_metric_image_nam:10,get_metrics_over_all_trans_with_init_valu:1,get_radar_plots_avg_plot:10,get_range_results_work:1,get_reference_imag:2,get_reference_image_nam:2,get_single_transform_im:1,get_trans_dict_from_str:10,get_transform_imag:10,get_transform_range_plot:10,get_transformed_image_nam:10,github:[5,14,16,17,18],give:[5,18,19],given:[1,5,7,9,10,19],go:[7,16,17,18],goal:19,gpu:12,gradient:7,graph:[0,1,10,12,14],graphic:[12,19],greycal:3,grip:17,group:[7,19],gui:12,gui_util:[0,15],h:[6,9],ha:[6,12,18],half:10,handl:12,handler:0,hardwar:12,harminc:6,have:[5,7,9,10,14,16,19],headless:13,height:[7,8],helper:10,here:18,high:[1,6],higher:[1,9],highest:12,hold:[6,7,8,10],home:[0,1,17],hook:6,horizont:9,hover_scatt:10,how:[5,10,14,16,17,18],html:17,http:[1,5,7,16,17,18],hue:9,human:[18,19],human_exp_csv:2,human_scor:10,i:[1,7,19],ident:[7,9],ignor:[6,7],im:[6,10],im_comp:5,im_ref:5,im_siz:8,imag:[0,2,3,5,6,7,8,9,10,12,14,15,18,19],image1:17,image2:17,image_display_s:1,image_list:2,image_list_to_transform:2,image_load:2,image_nam:1,image_path:10,image_post_process:2,image_postprocess:1,image_pre_process:2,image_preprocess:1,image_util:[0,15],img:[3,10],implement:[6,7,8,12],improv:12,includ:[7,12,16,17],increas:9,ind:10,independ:7,index:[5,13,14,19],individu:10,info:1,inform:[17,18],init:[1,17],init_layout:1,init_styl:1,init_valu:17,init_widget:1,init_worker_thread:1,initi:10,initialis:[1,6,7],input:[0,6,7,8,17],inspect:14,instanc:[5,6],instead:[6,10,17],integ:[6,7],interact:19,interfac:12,interpol:7,introduc:6,invari:19,investig:14,io:17,ipynb:[16,17,18],iqm:[0,1,2,10,13,15,16,17,18],iqm_vi:[13,14,16,17],item:[10,16],iter:1,its:[0,9,10],itself:19,ival:1,j:[1,7],johann:7,jpeg:[9,17],jpeg_compress:[9,17],jpg:17,just:[7,10,19],k1:5,k2:5,k:6,keep:8,keep_siz:10,kei:[1,2,10],kept:7,kernel:[7,9,17],kernel_s:[7,9],keyword:5,know:13,kodak:[0,15],kwarg:[1,2,5],l:6,label:[1,10],laparra:5,lapeva:5,laplacian:5,laplacianpyramid:6,laplacianpyramidgdn:6,larger:7,last:6,later:17,latest:13,latter:6,launch:[16,18],launch_experi:1,layer:[5,6],layout:[0,15],learn:[5,19],learnabl:7,learnt:8,left:1,lend:19,length:[6,10],less:[6,9],let:17,level:6,librari:13,libxcb:13,light:1,like:[8,19],lim:10,line_plott:10,link:13,linux:13,list1:1,list2:1,list:[1,2,6,8,10,17],lit:6,literatur:19,littl:17,load:[1,2,6,10,13,18],load_and_calibrate_imag:3,load_human_experi:1,load_imag:[2,10],load_image_list:2,load_json_dict:10,load_new_images_fold:1,load_obj:10,loader:2,local:[5,17],log:6,log_rad:6,longest:10,look:10,loss:[5,19],low:[1,6],lower:1,lowpass:6,lpip:5,lumin:[5,12,16,18],mae:[5,17],mai:[13,19],main:[0,15,16,17,18],main_menu:1,maintain:8,make:[0,10,13,14,18],make_app:1,make_experi:1,make_menu:1,make_name_for_tran:1,make_status_bar:1,make_ui:[0,16,17],maker:17,maketh:1,making_the_ui:16,manag:[12,14],mani:12,math:7,matlab:8,matplotlib:10,matrix:7,matt:[0,1,17],mattclifford1:[16,17,18],max:[10,17],max_lumin:3,maximum:16,mean:[5,19],measur:[5,16,19],menu:[1,16,18],meshgrid:6,meshgrid_angl:6,meta_dict:3,meter:16,method:10,metric:[0,1,2,3,10,12,14,15,18,19],metric_imag:[1,2,17],metric_param:[0,1,10],metric_range_graph:1,metric_scor:10,metrics_avg_graph:[0,1],metrics_info_format:[0,1],metrics_nam:10,metrics_to_us:[2,10],might:18,mild:5,mimic:19,min:[10,17],minimum:7,mismatch:13,model:[6,7,8,19],modul:[14,15],more:[12,17],most:18,mousepressev:1,mplcanva:10,ms_ssim:5,mse:[1,5,17],mse_imag:17,mssim_kernel_s:5,much:19,multi:[5,6],multipl:[0,15],multipli:7,must:[5,6,7],n:[13,16,18],n_channel:7,name:[1,2,10],navig:16,necessari:19,need:[0,1,6,8,16,17,18],net:1,network:[5,7],newer:13,nlpd:5,nlpd_k:5,nlpd_torch:[0,5],nn:[6,7],nois:[5,9],noise_ratio:5,non:[10,17],none:[0,1,2,6,7,10],normal:[7,9,10,17],normalis:[5,7,17],note:10,notebook:[16,17,18],nov:7,now:17,np:[5,9,10],num_orient:6,num_step:10,num_trans_valu:1,number:[6,7,9,16],numpi:[10,12],object:[0,1,5,10,19],observ:19,obtain:19,oct:6,octav:6,odd:[9,17],offer:14,offset:7,often:[13,19],onc:18,one:6,one_over_psnr:5,onli:[6,7,9,10,16,17,18],opencv:[12,13],oper:[7,17,19],optimis:6,option:[2,6,7,12,17,18],order:[1,6,7,12,18],orderpi:6,ordin:12,org:[5,7],orient:6,origin:[6,10],other:[10,12],otherwis:7,out:[9,10,12],output:[7,8],over:[5,6,7,10,16,17],overridden:6,overse:19,own:[17,18],p:6,packag:[13,14,15,17],packg:16,pad:[7,8],pair:[5,12],pairwis:18,paper:[5,6],param:1,param_group:1,paramet:[2,5,6,7,8,9,10,14,16,19],paramt:[10,16],particip:[12,18],particular:12,partit:1,pass:[6,7,17],past:16,patch:5,path:[1,2,10,17],pbar_sign:10,pdf:5,peak:5,peak_sign:5,peic:17,pepper:9,per:16,perceiv:[12,19],percentag:[9,10],percept:19,perceptu:[5,19],perform:[6,14,19],pick:12,pickl:10,pickle_path:10,pip:13,pivot:1,pixel:9,pkl:10,place:16,platform:13,plethora:19,plot:[1,10,12,18],plot_radar_graph:1,plot_util:[0,15],plu:10,plugin:13,point:[1,5,10,18],polar:10,posit:7,post:10,practition:[12,14,19],pre:12,precomput:6,premis:19,presenc:19,press:18,pretarin:6,pretrain:[5,6],previou:18,principl:19,print:17,prob:9,probabl:9,procedur:14,process:[6,10,12,17,19],produc:[16,19],profil:19,progress:1,progressbar:1,project:[16,17],properti:[0,2,12,14],proport:9,propos:[5,7],provid:[5,12,14,16,17],psnr:5,psychophys:19,pypi:13,pyqt6:[0,1,10,12],pyqt:[1,13],pyramid:[0,5,8],pyramid_filt:[5,6],python:[12,13,16],pythontutori:1,pytorch:[5,12],qcloseev:1,qlabel:1,qmainwindow:1,qmouseev:1,qobject:1,qprogressbar:1,qt:13,qtcore:1,qthread:1,qtwidget:1,qualit:[17,19],qualiti:[5,9,12,14,17,19],quantit:19,quick:[12,18],quick_sort:1,quit:1,radar:10,radar_nam:10,radar_plott:10,radial:6,radian:6,rais:[6,7],ranc:10,rang:[1,9,10,16,17,19],rate:19,ratio:5,reach:7,read:18,readi:18,real:12,recent:19,recip:6,recommend:[13,16],recreat:19,recurs:12,redo_plot:1,reduc:5,reduct:5,refer:[2,5,10,12,19],region:6,regist:6,reinstal:13,remain:19,reparam_offset:7,reparameteris:7,repons:14,repres:7,request_range_work:1,requir:[1,13,16,17,18,19],reset_correlation_data:1,reset_experi:1,reset_slid:1,reset_slider_group:1,residu:6,resiz:[10,12],resize_imag:10,resize_to_longest_sid:10,respect:[12,19],respons:19,restrict_opt:[0,1],result:[1,10,12,14],results_ord:10,return_dict:10,return_imag:[5,17],rgb:10,rgb_bright:[1,10],right:1,robust:5,rotat:[2,6,9,12,16,17],round:14,run:[3,6,7,12,13,14,16],running_an_experi:18,s:[17,19],salt:9,salt_and_pepper_nois:9,same:[2,5,6,7,8,19],sampl:[5,9],sat:9,satur:9,save:[1,10,16,18],save_experi:1,save_experiment_result:10,save_imag:10,save_json_dict:10,save_obj:10,save_util:[0,15],saved_experi:1,scalar:[5,17],scale:[5,6],scale_factor:[9,10],scatter:10,scatter_plott:10,scenario:[14,19],score:[5,12,18],scratch:13,screen:[12,16],script:16,second:[6,19],secondli:14,see:[12,14,17,18],select:[12,14,16,18],self:1,send:10,sent:1,sepcifici:6,serv:19,set:[1,6,14,18],set_checked_menu_from_iter:1,set_image_name_text:1,set_plot_lim:10,set_styl:10,setup:[1,18],setup_experi:1,shape:[7,8],shift:9,should:[6,7,13],show:[0,10,12,18],show_all_imag:1,shown:18,side:10,sigma:5,signal:[1,5,10],silent:6,similar:[5,17,18,19],simon1995:8,simon1995pyr:6,simoncelli:6,simpl:[0,12,14,15],simpler:10,simplest:19,sinc:[6,17],singl:10,single_trans_dict:1,singular:6,size:[3,6,7,8,9,10,12,18],skimag:9,small:10,smaller:16,smoother:1,so:[1,10,12,13],softwar:19,some:[13,16,17],sort:[1,12,18],sort_list:1,sourc:[0,1,2,3,5,6,7,8,9,10],space:19,spacial:[14,17],spatial:[6,7,8],specif:[7,12,19],specifi:[6,10,17],spider:10,sqrt:7,squar:[5,7,8,9,10,16,19],squeez:5,ssim:[5,14,17,19],ssim_imag:17,stack:6,stage:6,stanard:12,standard:12,start:[9,17,18],start_experi:1,state:1,steer_matrix:6,steerabl:[6,8],steerablepyramid:6,steerablewavelet:6,stop:1,stop_flag:10,stopped_range_result:1,storag:12,store:[2,8,17],str:[0,5],str_to_len:10,straightforward:12,strictli:5,stride:[7,8],string:10,structur:[5,19],style:1,subband:6,subclass:[1,6],submodul:15,subpackag:15,subtract:5,sudo:13,sum:5,sum_j:7,sure:[0,13,14,18],swap_ind:1,system:5,t:6,tab:[1,16],take:[5,6,12,16,18],taken:8,task:12,tensor:[6,7],test:14,test_datastore_attribut:0,text:10,textur:5,than:[1,6,7,9],theh:16,thei:[2,7,18,19],them:[1,6,17],thereon:6,theta:6,thi:[6,7,8,10,12,13,16,17,18,19],thing:18,thread:[0,15],threshold:9,through:[6,12,14,16,17,18],timescal:12,todo:[0,6,10],toggle_experi:1,too:19,toolbox:14,torch:[6,7],tradit:19,train:[6,7],trainabl:6,tran:[1,10],trans_nam:10,trans_str:[1,10],transform:[0,1,2,3,5,6,7,10,12,14,15,18],transform_funct:10,transform_param:10,transform_valu:10,transformation_nam:10,transformed_imag:2,transit:6,translat:[9,12],treat:7,tree:[16,17,18],truthfulli:12,tutori:12,tutorial_1:16,tutorial_2:17,tutorial_3:18,twidth:6,two:[5,6,14,17,19],txt:1,type:[5,6,7,8,9,10],typeerror:[6,7],ubyt:10,ui:[0,2,5,10,14,15,17,18],ui_wrapp:15,unchang:19,under:14,underli:12,understand:[12,14],undistort:12,uninstal:13,union:6,unsort:1,until:18,up:[1,14,17],update_annot:10,update_image_set:1,update_progress:1,update_status_bar:1,upsampl:6,upsample_output:6,us:[1,2,5,6,7,8,9,10,12,13,16,17,18],usag:0,user:[9,12,14,18],util:[0,2,5,6,15],utilis:19,uv:5,v:1,valero:5,valu:[2,5,6,7,9,10,16,17],var_nam:10,var_valu:10,varianc:5,variou:14,version:13,vertic:9,vgg:5,vi:[0,1,2,13,16,17,18,19],via:[1,2],view:[12,16,17,18],view_correlation_inst:1,virtual:13,visibl:19,visit:14,visual:[5,14],visualis:[12,14],w:6,wa:10,wai:14,want:[17,18],washington:6,wavelet:6,wavelet_transform:6,waves1:17,waves2:17,we:[1,16,17,18,19],weight:[6,7],well:[12,13,14],what:0,when:[5,7,10,16,17,18],where:[6,7,19],whether:[5,6,7],which:[2,5,8,10,12,14,19],whole:[10,16,17,18],why:19,widget:[0,10,15],widget_nam:1,width:[6,7,8],wiki:5,wikipedia:5,window:1,wise:7,within:[6,16],without:14,work:13,worker:1,world:12,would:16,write:[0,10,14],www:[1,5],x1:6,x2:6,x:[6,7,10],x_label:10,x_shift:9,xcosn:6,xrco:6,y:[7,10,13],y_label:10,y_shift:9,ycosn:6,yirco:6,you:[13,14,16,17,18],your:[17,18],yrco:6,zero:[7,17],zoom:[9,10],zoom_imag:9},titles:["IQM_Vis package","IQM_Vis.UI package","IQM_Vis.data_handlers package","IQM_Vis.examples package","IQM_Vis.examples.images package","IQM_Vis.metrics package","IQM_Vis.metrics.NLPD_torch package","IQM_Vis.metrics.NLPD_torch.layers package","IQM_Vis.metrics.NLPD_torch.utils package","IQM_Vis.transformations package","IQM_Vis.utils package","Tutorials","About IQM-Vis","Getting Started","IQM-Vis documentation","IQM_Vis","Tutorial 1: Making the UI","Tutorial 2: Simple Customisation","Tutorial 3: Running an Experiment","IQMs"],titleterms:{"1":16,"2":17,"3":18,"function":12,For:19,about:[12,14],ad:16,all:[3,17],an:[14,18,19],analysi:14,bright:16,built:12,choos:19,code:14,common:13,content:[0,1,2,3,4,5,6,7,8,9,10],conv:8,correl:14,custom_widget:1,customis:17,data_api:2,data_api_abstract:2,data_handl:2,dataset:3,differ:19,dispali:16,displai:16,dist:3,divisive_normalis:7,document:14,exampl:[3,4],experi:[3,12,16,18],experiment_mod:1,finsih:18,fourier:8,get:[13,14],graph:16,gui_util:10,how:19,human:[12,14],imag:[1,4,16,17],image_util:10,indic:14,info:18,instal:13,iqm:[5,12,14,19],iqm_vi:[0,1,2,3,4,5,6,7,8,9,10,15],issu:13,kodak:3,layer:7,layout:1,load:16,main:1,make:16,max:16,metric:[5,6,7,8,16,17],modul:[0,1,2,3,4,5,6,7,8,9,10],multipl:3,nlpd_torch:[6,7,8],offer:12,other:16,own:16,packag:[0,1,2,3,4,5,6,7,8,9,10],percept:[12,14],plot_util:10,post:16,pre:16,process:16,put:17,pyramid:6,pyramid_filt:8,qualit:14,quantit:14,result:18,rgb:16,run:18,save_util:10,screen:18,set:16,simpl:[3,17],size:16,softwar:12,sourc:14,start:[13,14],step:16,submodul:[0,1,2,3,5,6,7,8,9,10],subpackag:[0,3,5,6],tabl:14,task:19,test:13,thread:1,togeth:17,transform:[9,16,17],tutori:[11,14,16,17,18],type:19,ui:[1,16],ui_wrapp:0,util:[1,8,10],vi:[12,14],visualis:18,what:[12,14,19],widget:1,your:[16,19]}})