Search.setIndex({docnames:["IQM_Vis","IQM_Vis.UI","IQM_Vis.data_handlers","IQM_Vis.examples","IQM_Vis.examples.images","IQM_Vis.metrics","IQM_Vis.metrics.NLPD_torch","IQM_Vis.metrics.NLPD_torch.layers","IQM_Vis.metrics.NLPD_torch.utils","IQM_Vis.transformations","IQM_Vis.utils","Tutorials","about","getting_started","index","modules","notebooks/Tutorial_1-making_the_UI","notebooks/Tutorial_2-Customisation","notebooks/Tutorial_3-Advanced-Customisations","notebooks/Tutorial_4-running_an_experiment","what-are-IQMs"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":5,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.viewcode":1,nbsphinx:4,sphinx:56},filenames:["IQM_Vis.rst","IQM_Vis.UI.rst","IQM_Vis.data_handlers.rst","IQM_Vis.examples.rst","IQM_Vis.examples.images.rst","IQM_Vis.metrics.rst","IQM_Vis.metrics.NLPD_torch.rst","IQM_Vis.metrics.NLPD_torch.layers.rst","IQM_Vis.metrics.NLPD_torch.utils.rst","IQM_Vis.transformations.rst","IQM_Vis.utils.rst","Tutorials.rst","about.rst","getting_started.rst","index.rst","modules.rst","notebooks/Tutorial_1-making_the_UI.ipynb","notebooks/Tutorial_2-Customisation.ipynb","notebooks/Tutorial_3-Advanced-Customisations.ipynb","notebooks/Tutorial_4-running_an_experiment.ipynb","what-are-IQMs.rst"],objects:{"":[[0,0,0,"-","IQM_Vis"]],"IQM_Vis.UI":[[1,0,0,"-","custom_widgets"],[1,0,0,"-","experiment_mode"],[1,0,0,"-","images"],[1,0,0,"-","layout"],[1,0,0,"-","main"],[1,0,0,"-","threads"],[1,0,0,"-","utils"],[1,0,0,"-","widgets"]],"IQM_Vis.UI.custom_widgets":[[1,1,1,"","ClickLabel"],[1,1,1,"","ProgressBar"]],"IQM_Vis.UI.custom_widgets.ClickLabel":[[1,2,1,"","clicked"],[1,3,1,"","mousePressEvent"]],"IQM_Vis.UI.experiment_mode":[[1,1,1,"","make_experiment"],[1,4,1,"","make_name_for_trans"],[1,4,1,"","sort_list"]],"IQM_Vis.UI.experiment_mode.make_experiment":[[1,3,1,"","change_experiment_images"],[1,3,1,"","clicked_image"],[1,3,1,"","closeEvent"],[1,3,1,"","experiment_layout"],[1,3,1,"","finish_experiment"],[1,3,1,"","get_all_images"],[1,3,1,"","get_single_transform_im"],[1,3,1,"","init_style"],[1,3,1,"","partition"],[1,3,1,"","quick_sort"],[1,3,1,"","quit"],[1,3,1,"","reset_experiment"],[1,3,1,"","save_experiment"],[1,2,1,"","saved_experiment"],[1,3,1,"","setup_experiment"],[1,3,1,"","show_all_images"],[1,3,1,"","start_experiment"],[1,3,1,"","swap_inds"],[1,3,1,"","toggle_experiment"]],"IQM_Vis.UI.images":[[1,1,1,"","images"]],"IQM_Vis.UI.images.images":[[1,3,1,"","change_data"],[1,3,1,"","change_metric_correlations_graph"],[1,3,1,"","change_metric_range_graph"],[1,3,1,"","change_to_specific_trans"],[1,3,1,"","completed_range_results"],[1,3,1,"","display_images"],[1,3,1,"","display_metric_correlation_plot"],[1,3,1,"","display_metric_images"],[1,3,1,"","display_metric_range_plot"],[1,3,1,"","display_metrics"],[1,3,1,"","display_metrics_graph"],[1,3,1,"","display_metrics_text"],[1,3,1,"","display_radar_plots"],[1,3,1,"","get_metrics_over_all_trans_with_init_values"],[1,3,1,"","init_worker_thread"],[1,3,1,"","load_human_experiment"],[1,3,1,"","load_new_images_folder"],[1,3,1,"","plot_radar_graph"],[1,3,1,"","redo_plots"],[1,2,1,"","request_range_work"],[1,3,1,"","stopped_range_results"],[1,2,1,"","view_correlation_instance"]],"IQM_Vis.UI.layout":[[1,1,1,"","layout"]],"IQM_Vis.UI.layout.layout":[[1,3,1,"","init_layout"],[1,3,1,"","init_style"]],"IQM_Vis.UI.main":[[1,1,1,"","make_app"],[1,4,1,"","set_checked_menu_from_iterable"]],"IQM_Vis.UI.main.make_app":[[1,3,1,"","change_save_folder"],[1,3,1,"","closeEvent"],[1,3,1,"","construct_UI"],[1,3,1,"","get_menu_checkboxes"],[1,3,1,"","make_menu"],[1,3,1,"","make_status_bar"],[1,3,1,"","quit"],[1,3,1,"","reset_correlation_data"]],"IQM_Vis.UI.threads":[[1,1,1,"","get_range_results_worker"]],"IQM_Vis.UI.threads.get_range_results_worker":[[1,2,1,"","completed"],[1,2,1,"","current_image"],[1,3,1,"","do_work"],[1,2,1,"","progress"],[1,3,1,"","stop"],[1,2,1,"","stopped"]],"IQM_Vis.UI.utils":[[1,4,1,"","add_layout_to_tab"]],"IQM_Vis.UI.widgets":[[1,1,1,"","widgets"]],"IQM_Vis.UI.widgets.widgets":[[1,3,1,"","change_display_im_display_brightness"],[1,3,1,"","change_display_im_rgb_brightness"],[1,3,1,"","change_display_im_size"],[1,3,1,"","change_graph_size"],[1,3,1,"","change_human_scores_after_exp"],[1,3,1,"","change_num_steps"],[1,3,1,"","change_plot_lims"],[1,3,1,"","change_post_processing"],[1,3,1,"","change_pre_processing"],[1,3,1,"","display_slider_num"],[1,3,1,"","generic_value_change"],[1,3,1,"","init_widgets"],[1,3,1,"","launch_experiment"],[1,3,1,"","reset_slider_group"],[1,3,1,"","reset_sliders"],[1,3,1,"","set_image_name_text"],[1,3,1,"","update_image_settings"],[1,3,1,"","update_progress"],[1,3,1,"","update_status_bar"]],"IQM_Vis.data_handlers":[[2,0,0,"-","data_api"],[2,0,0,"-","data_api_abstract"]],"IQM_Vis.data_handlers.data_api":[[2,1,1,"","dataset_holder"]],"IQM_Vis.data_handlers.data_api.dataset_holder":[[2,3,1,"","get_image_to_transform"],[2,3,1,"","get_image_to_transform_name"],[2,3,1,"","get_metric_images"],[2,3,1,"","get_metrics"],[2,3,1,"","get_reference_image"],[2,3,1,"","get_reference_image_name"],[2,3,1,"","load_image_list"]],"IQM_Vis.data_handlers.data_api_abstract":[[2,1,1,"","base_dataloader"],[2,1,1,"","base_dataset_loader"]],"IQM_Vis.data_handlers.data_api_abstract.base_dataloader":[[2,3,1,"","get_image_to_transform"],[2,3,1,"","get_image_to_transform_name"],[2,3,1,"","get_metric_images"],[2,3,1,"","get_metrics"],[2,3,1,"","get_reference_image"],[2,3,1,"","get_reference_image_name"],[2,5,1,"","metric_images"],[2,5,1,"","metrics"]],"IQM_Vis.examples":[[3,0,0,"-","all"],[3,0,0,"-","dataset"],[3,0,0,"-","dists"],[3,0,0,"-","experiment"],[4,0,0,"-","images"],[3,0,0,"-","kodak"],[3,0,0,"-","multiple"],[3,0,0,"-","simple"]],"IQM_Vis.examples.all":[[3,4,1,"","run"]],"IQM_Vis.examples.dataset":[[3,4,1,"","run"]],"IQM_Vis.examples.dists":[[3,4,1,"","correct"],[3,4,1,"","load_and_calibrate_image"],[3,4,1,"","run"]],"IQM_Vis.examples.experiment":[[3,4,1,"","run"]],"IQM_Vis.examples.kodak":[[3,4,1,"","run"]],"IQM_Vis.examples.multiple":[[3,4,1,"","run"]],"IQM_Vis.examples.simple":[[3,4,1,"","run"]],"IQM_Vis.metrics":[[5,0,0,"-","IQMs"],[6,0,0,"-","NLPD_torch"],[5,4,1,"","get_all_IQM_params"],[5,4,1,"","get_all_metric_images"],[5,4,1,"","get_all_metrics"]],"IQM_Vis.metrics.IQMs":[[5,1,1,"","DISTS"],[5,1,1,"","LPIPS"],[5,1,1,"","MAE"],[5,1,1,"","MSE"],[5,1,1,"","MS_SSIM"],[5,1,1,"","NLPD"],[5,1,1,"","SSIM"],[5,1,1,"","one_over_PSNR"]],"IQM_Vis.metrics.IQMs.DISTS":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.LPIPS":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.MAE":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.MSE":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.MS_SSIM":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.NLPD":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.SSIM":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.IQMs.one_over_PSNR":[[5,3,1,"","__call__"]],"IQM_Vis.metrics.NLPD_torch":[[7,0,0,"-","layers"],[6,0,0,"-","pyramids"],[8,0,0,"-","utils"]],"IQM_Vis.metrics.NLPD_torch.layers":[[7,0,0,"-","divisive_normalisation"]],"IQM_Vis.metrics.NLPD_torch.layers.divisive_normalisation":[[7,1,1,"","GDN"]],"IQM_Vis.metrics.NLPD_torch.layers.divisive_normalisation.GDN":[[7,2,1,"","beta"],[7,2,1,"","beta_reparam"],[7,3,1,"","clamp_parameters"],[7,3,1,"","forward"],[7,2,1,"","gamma"],[7,2,1,"","groups"],[7,2,1,"","reparam_offset"],[7,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.pyramids":[[6,1,1,"","LaplacianPyramid"],[6,1,1,"","LaplacianPyramidGDN"],[6,1,1,"","SteerablePyramid"],[6,1,1,"","SteerableWavelet"]],"IQM_Vis.metrics.NLPD_torch.pyramids.LaplacianPyramid":[[6,3,1,"","DN_filters"],[6,3,1,"","forward"],[6,3,1,"","pyramid"],[6,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.pyramids.LaplacianPyramidGDN":[[6,3,1,"","compare"],[6,3,1,"","pyramid"],[6,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.pyramids.SteerablePyramid":[[6,2,1,"","TODO"],[6,3,1,"","forward"],[6,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.pyramids.SteerableWavelet":[[6,2,1,"","Xcosn"],[6,2,1,"","Xrcos"],[6,2,1,"","YIrcos"],[6,2,1,"","Ycosn"],[6,2,1,"","Yrcos"],[6,2,1,"","angles"],[6,2,1,"","const"],[6,3,1,"","forward"],[6,2,1,"","harmincs"],[6,3,1,"","meshgrid_angle"],[6,2,1,"","num_orientations"],[6,2,1,"","steer_matrix"],[6,2,1,"","training"]],"IQM_Vis.metrics.NLPD_torch.utils":[[8,0,0,"-","conv"],[8,0,0,"-","pyramid_filters"]],"IQM_Vis.metrics.NLPD_torch.utils.conv":[[8,4,1,"","pad"]],"IQM_Vis.transformations":[[9,4,1,"","get_all_transforms"],[9,0,0,"-","transforms"]],"IQM_Vis.transformations.transforms":[[9,4,1,"","binary_threshold"],[9,4,1,"","blur"],[9,4,1,"","brightness"],[9,4,1,"","brightness_hsv"],[9,4,1,"","contrast"],[9,4,1,"","hue"],[9,4,1,"","jpeg_compression"],[9,4,1,"","rotation"],[9,4,1,"","salt_and_pepper_noise"],[9,4,1,"","saturation"],[9,4,1,"","x_shift"],[9,4,1,"","y_shift"],[9,4,1,"","zoom_image"]],"IQM_Vis.ui_wrapper":[[0,1,1,"","make_UI"],[0,4,1,"","test_datastore_attributes"]],"IQM_Vis.ui_wrapper.make_UI":[[0,3,1,"","show"]],"IQM_Vis.utils":[[10,0,0,"-","gui_utils"],[10,0,0,"-","image_utils"],[10,0,0,"-","plot_utils"],[10,0,0,"-","save_utils"]],"IQM_Vis.utils.gui_utils":[[10,1,1,"","MplCanvas"],[10,4,1,"","change_im"],[10,4,1,"","get_image_pair_name"],[10,4,1,"","get_metric_image_name"],[10,4,1,"","get_trans_dict_from_str"],[10,4,1,"","get_transformed_image_name"],[10,4,1,"","str_to_len"]],"IQM_Vis.utils.image_utils":[[10,4,1,"","calibrate_brightness"],[10,4,1,"","crop_centre"],[10,4,1,"","get_transform_image"],[10,4,1,"","load_image"],[10,4,1,"","resize_image"],[10,4,1,"","resize_to_longest_side"],[10,4,1,"","save_image"]],"IQM_Vis.utils.plot_utils":[[10,1,1,"","bar_plotter"],[10,4,1,"","click_scatter"],[10,4,1,"","compute_metric_for_human_correlation"],[10,4,1,"","compute_metrics_over_range"],[10,4,1,"","compute_metrics_over_range_single_trans"],[10,4,1,"","get_all_single_transform_params"],[10,4,1,"","get_all_slider_values"],[10,4,1,"","get_correlation_plot"],[10,4,1,"","get_radar_plots_avg_plots"],[10,4,1,"","get_transform_range_plots"],[10,4,1,"","hover_scatter"],[10,1,1,"","line_plotter"],[10,1,1,"","radar_plotter"],[10,1,1,"","scatter_plotter"],[10,4,1,"","update_annot"]],"IQM_Vis.utils.plot_utils.bar_plotter":[[10,3,1,"","plot"],[10,3,1,"","set_plot_lims"],[10,3,1,"","set_style"],[10,3,1,"","show"]],"IQM_Vis.utils.plot_utils.line_plotter":[[10,3,1,"","plot"],[10,3,1,"","set_plot_lims"],[10,3,1,"","set_style"],[10,3,1,"","show"]],"IQM_Vis.utils.plot_utils.radar_plotter":[[10,3,1,"","plot"],[10,3,1,"","set_plot_lims"],[10,3,1,"","set_style"],[10,3,1,"","show"]],"IQM_Vis.utils.plot_utils.scatter_plotter":[[10,3,1,"","plot"],[10,3,1,"","set_plot_lims"],[10,3,1,"","set_style"],[10,3,1,"","show"]],"IQM_Vis.utils.save_utils":[[10,4,1,"","load_json_dict"],[10,4,1,"","load_obj"],[10,4,1,"","save_experiment_results"],[10,4,1,"","save_json_dict"],[10,4,1,"","save_obj"]],IQM_Vis:[[1,0,0,"-","UI"],[2,0,0,"-","data_handlers"],[3,0,0,"-","examples"],[5,0,0,"-","metrics"],[9,0,0,"-","transformations"],[0,0,0,"-","ui_wrapper"],[10,0,0,"-","utils"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","function","Python function"],"5":["py","property","Python property"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:function","5":"py:property"},terms:{"0":[5,7,9,10,16,17,18],"01":5,"03":5,"06":7,"06281v4":7,"1":[1,5,6,7,9,10,14,17,18],"100":[9,10,17],"101":9,"11":[5,10],"128":10,"150":1,"1511":7,"18":7,"180":17,"1995":6,"1e":7,"2":[6,7,9,10,14,18],"200":3,"2015":7,"2016_hvei":5,"250":10,"255":9,"256":3,"2x":[9,10],"3":[6,7,10,13,14,17],"39":17,"4":[6,14,17,18],"41":17,"5":[1,5,9,10,16,17,18],"6":[1,7,17,18],"7":[9,18],"8":18,"814697265625e":7,"9":13,"90":9,"abstract":2,"ball\u00e9":7,"boolean":[6,7],"class":[0,1,2,5,6,7,10,18],"const":6,"default":[2,5,6,7,9,10,16,18],"do":[10,12,13,14,16],"float":[6,7,9,10,17,18],"function":[1,2,6,7,8,10,16,17,18,20],"import":[13,16,17,18,20],"int":[6,7,8,9,17],"new":[1,13,16],"return":[5,6,7,8,9,10,17,18,19],"true":[0,1,3,5,6,7,10,17],"try":13,"while":6,A:[6,7,18],For:[2,17,18],If:[2,6,7,13,19],In:[7,16,17,18,19,20],It:[5,12,13,20],On:19,The:[5,6,7,8,12,16,19,20],Then:[6,13,18],There:[13,20],These:[14,17,20],To:[16,17,19],_:8,__call__:[5,18],__init__:[6,18],_plot:10,_redo_plot:1,_variablefunctionsclass:6,a0:1,a_tran:1,ab:[7,18],abc:2,abl:14,about:[1,18],abov:18,absolut:5,acceler:12,access:[0,12],accord:20,achiev:12,across:10,act:7,action_stor:1,activ:[7,13],ad:[12,17],add:[1,9,16,18],add_layout_to_tab:1,adher:20,adjust:[9,16,18],advanc:18,advantag:12,after:[2,10,16],afterward:6,against:[12,19],aim:20,al:[5,7],alex:5,algorithm:[12,19,20],align:5,all:[0,1,2,5,6,8,9,10,15,16,19],also:[7,12,13,17,18,20],although:6,alwai:7,amount:[6,8,9],an:[1,2,5,6,7,9,12,16,17],anaconda:13,analys:[12,14],analysi:[12,17],angl:[6,9],angular:6,ani:[12,14,16,18],annot:10,anyth:18,api:[0,2],app:1,append_char:10,appli:[1,2,7,16,20],apply_independ:7,approach:7,apt:13,ar:[0,1,2,5,6,7,8,9,12,13,14,18,19,20],arbitrari:5,architectur:6,area:9,arg:[1,18],argument:[5,18],around:[9,13],arrai:[1,5,9,10,18],arxiv:7,aspect:17,associ:5,assum:8,att:18,attempt:20,attribut:[0,18],automat:12,avaiabl:3,avail:5,avoid:7,ax:10,b:[9,16,19],b_tran:1,backend:[5,10,12],backend_qtagg:10,backpropog:7,balle2015gdn:7,band:6,bar:16,bar_nam:10,bar_plott:10,base:[0,1,2,5,6,7,10],base_dataload:2,base_dataset_load:2,basic:17,batch:5,batch_siz:7,been:6,befor:[16,17],behav:14,behaviour:20,being:[8,10,20],benchmark:20,best:[10,20],beta:7,beta_min:7,beta_reparam:7,better:9,between:[1,5,20],beyond:9,bia:7,binari:9,binary_threshold:9,black:[9,16],blank:16,blueprint:2,blur:[9,17],boarder:16,bool:[0,5,6,7,10],both:[2,20],bound:18,box:12,bright:[9,17,18],brightness_hsv:9,bundl:17,button:[1,19],calc_rang:1,calcul:[1,8,12,16],calibr:[12,19],calibrate_bright:10,call:[5,6,7,16,18],callabl:[2,18],can:[1,7,12,13,14,16,17,18,19,20],candela:16,capabilit:12,captur:20,care:6,carefulli:7,categoris:20,centr:[9,10],chang:[1,10,13,16,17],change_data:1,change_display_im_display_bright:1,change_display_im_rgb_bright:1,change_display_im_s:1,change_experiment_imag:1,change_graph_s:1,change_human_scores_after_exp:1,change_im:10,change_metric_correlations_graph:1,change_metric_range_graph:1,change_num_step:1,change_plot_lim:1,change_post_process:1,change_pre_process:1,change_save_fold:1,change_to_specific_tran:1,change_trans_value_sign:10,channel:7,checked_transform:1,choos:5,chosen:7,clamp:7,clamp_paramet:7,clash:13,click:[1,10,16,19],click_scatt:10,clickabl:1,clicked_imag:1,clicklabel:1,clip:[9,18],close:7,closeev:1,co:6,code:[5,10,13],collect:12,com:[5,16,17,18,19],commun:2,comp:17,compar:[6,12,17,19,20],comparison:[5,12,18],complet:1,completed_range_result:1,comprehens:14,compress:9,comput:[6,10,16],compute_metric_for_human_correl:10,compute_metrics_over_rang:10,compute_metrics_over_range_single_tran:10,conda:13,conduct:[12,14],conf:6,conform:[12,14],connect_func:1,consist:20,construct_ui:1,constructor:2,contain:[6,8,10,16,19],content:15,context:20,contrast:9,control:5,conv:[5,6],conveni:12,conver:9,convert:9,convoltuion:7,convolut:[7,8,9],copi:16,correct:[0,3,12,19],correl:[10,12,19,20],correspond:[10,16,19],could:13,cover:12,creat:[1,13,20],crop:[2,10,12,16],crop_centr:10,crope:10,crucial:12,css_file:1,csv:19,current:10,current_imag:1,cursor0:13,custom:[1,12,17,18],custom_bright:18,custom_mae_class:18,custom_mae_funct:18,custom_widget:[0,15],customis:[14,19],data:[0,1,2,10,12,14,17,18,20],data_api:[0,10,15],data_api_abstract:[0,15],data_handl:[0,15],data_stor:[0,1,10],dataset:[0,1,10,12,13,15,18],dataset_hold:[2,17,18],datastor:17,dc:6,debug:0,decod:9,decreas:9,deep:[5,20],def:18,default_save_dir:[0,1],defin:[6,17,18],degre:9,demonstr:[13,14],densiti:7,depend:13,deriv:6,design:12,desir:[12,17],despit:20,detail:[12,14],determin:7,develop:12,dfferent:6,dict:[0,1,2,10],dict_:10,dictionari:[2,17,18],differ:[2,6,13,14],digit:9,dim:6,dimens:[5,6],dingkeyan93:5,directori:16,disagre:19,disp_len:1,displai:[12,19],display_bright:[1,10],display_imag:1,display_metr:1,display_metric_correlation_plot:1,display_metric_imag:1,display_metric_range_plot:1,display_metrics_graph:1,display_metrics_text:1,display_radar_plot:1,display_slider_num:1,dissimilar:5,dist:[0,5,15],distanc:20,distor:14,distort:[12,14,17,18,20],divid:7,divis:7,divisive_normalis:[5,6],divisv:7,dn_filter:6,do_work:1,doc:[0,10,16,17,18,19],document:[12,17],domain:[6,8],done:6,down:1,downsampl:6,dpi:10,drop:1,dtype:[6,7],dummi:18,dummy_arg:18,e:[5,6,13,14,16,18,20],each:[6,7,10],earli:5,effect:14,element:[1,6],empir:20,en:5,enabl:12,encod:9,entri:[1,6],environ:13,equal:7,error:[5,13,18,20],es:5,et:[5,7],etc:[0,19],euclidean:20,ev:1,evalu:[5,12,14,20],event:[1,10],everi:6,everyth:[17,19],exactli:18,exampl:[0,2,5,13,15,17,18,20],exeprt:8,expand:18,expect:14,expens:20,experi:[0,1,10,14,15,20],experiment:20,experiment_layout:1,experiment_mod:[0,15],expert:[6,7,8],expos:12,extent:1,extra:[13,18],extrem:20,f:17,facilit:[12,14],fail:12,fals:[0,1,5,6,7,10],featur:[12,14],feel:17,figur:10,figurecanvasqtagg:10,file:[2,3,10,16,17,19],filepath:17,fill:9,filt:6,filt_siz:8,filter:[6,8],finish_experi:1,first:[6,13,17,19,20],firstli:14,fix:10,flexibl:6,float32:9,folder:[1,16,19],follow:18,form:[12,18],former:6,forward:[6,7],fourier:[5,6],frame:10,framework:12,free:17,freeman:6,fresh:13,from:[1,2,5,6,8,10,12,13,16,19,20],further:[12,14],g:[5,13,14,16,18],gain:5,gamma:7,gamma_init:7,gan:5,gather:20,gaussian:9,gdn:7,gener:[2,5,7,12,19],generalis:7,generic_value_chang:1,geometr:5,get:[0,5,7,9,10,17],get_all_imag:1,get_all_iqm_param:5,get_all_metr:5,get_all_metric_imag:5,get_all_single_transform_param:10,get_all_slider_valu:10,get_all_transform:9,get_correlation_plot:10,get_image_pair_nam:10,get_image_to_transform:2,get_image_to_transform_nam:2,get_menu_checkbox:1,get_metr:2,get_metric_imag:2,get_metric_image_nam:10,get_metrics_over_all_trans_with_init_valu:1,get_radar_plots_avg_plot:10,get_range_results_work:1,get_reference_imag:2,get_reference_image_nam:2,get_single_transform_im:1,get_trans_dict_from_str:10,get_transform_imag:10,get_transform_range_plot:10,get_transformed_image_nam:10,github:[5,14,16,17,18,19],give:[5,19,20],given:[1,5,7,9,10,20],go:[7,16,17,19],goal:20,gpu:12,gradient:7,graph:[0,1,10,12,14],graphic:[12,20],greycal:3,grip:17,group:[7,20],gui:12,gui_util:[0,15],h:[6,9],ha:[6,12,19],half:10,handl:12,handler:0,hardwar:12,harminc:6,have:[5,7,9,10,14,16,18,20],headless:13,height:[7,8],helper:10,here:[18,19],high:[1,6],higher:[1,9],highest:12,hold:[6,7,8,10],home:[0,1,17,18],hook:6,horizont:9,hover_scatt:10,how:[5,10,14,16,17,19],html:17,http:[1,5,7,16,17,18,19],hue:9,human:[19,20],human_exp_csv:2,human_scor:10,i:[1,7,20],ident:[7,9],ignor:[6,7],illustr:14,im:[6,10],im_comp:[5,18],im_ref:[5,18],im_siz:8,imag:[0,2,3,5,6,7,8,9,10,12,14,15,18,19,20],image1:17,image2:17,image_display_s:1,image_list:2,image_list_to_transform:2,image_load:2,image_nam:1,image_path:10,image_post_process:2,image_postprocess:1,image_pre_process:2,image_preprocess:1,image_util:[0,15],img:[3,10],implement:[6,7,8,12],improv:12,includ:[7,12,16,17,18],increas:9,ind:10,independ:7,index:[5,13,14,20],individu:10,info:1,inform:[17,19],init:[1,17],init_layout:1,init_styl:1,init_valu:[17,18],init_widget:1,init_worker_thread:1,initi:10,initialis:[1,6,7,18],input:[0,6,7,8,17,18],inspect:14,instanc:[5,6],instead:[6,10,17],integ:[6,7],interact:20,interfac:12,interpol:7,introduc:6,invari:20,investig:14,io:17,ipynb:[16,17,18,19],iqm:[0,1,2,10,13,15,16,17,18,19],iqm_vi:[13,14,16,17,18],item:[10,16],iter:1,its:[0,9,10],itself:20,ival:1,j:[1,7],johann:7,jpeg:[9,17],jpeg_compress:[9,17],jpg:17,just:[7,10,20],k1:5,k2:5,k:6,keep:8,keep_siz:10,kei:[1,2,10,18],kept:7,kernel:[7,9,17],kernel_s:[7,9],keyword:5,know:13,kodak:[0,15,18],kodim01:18,kodim02:18,kwarg:[1,2,5,18],l1:18,l:6,label:[1,10],laparra:5,lapeva:5,laplacian:5,laplacianpyramid:6,laplacianpyramidgdn:6,larger:7,last:6,later:[17,18],latest:13,latter:6,launch:[16,19],launch_experi:1,layer:[5,6],layout:[0,15],learn:[5,20],learnabl:7,learnt:8,left:1,lend:20,length:[6,10],less:[6,9],let:[17,18],level:6,librari:13,libxcb:13,light:1,like:[8,18,20],lim:10,line_plott:10,link:13,linux:13,list1:1,list2:1,list:[1,2,6,8,10,17],lit:6,literatur:20,littl:17,load:[1,2,6,10,13,19],load_and_calibrate_imag:3,load_human_experi:1,load_imag:[2,10],load_image_list:2,load_json_dict:10,load_new_images_fold:1,load_obj:10,loader:2,local:[5,17],log:6,log_rad:6,longest:10,look:10,loss:[5,20],low:[1,6],lower:1,lowpass:6,lpip:5,lumin:[5,12,16,19],mae:[5,17,18],mai:[13,20],main:[0,15,16,17,18,19],main_menu:1,maintain:8,make:[0,10,13,14,19],make_app:1,make_experi:1,make_menu:1,make_name_for_tran:1,make_status_bar:1,make_ui:[0,16,17,18],maker:17,maketh:1,making_the_ui:16,manag:[12,14],mani:12,math:7,matlab:8,matplotlib:10,matrix:7,matt:[0,1,17,18],mattclifford1:[16,17,18,19],max:[10,17,18],max_lumin:3,maximum:16,mean:[5,18,20],measur:[5,16,20],menu:[1,16,19],meshgrid:6,meshgrid_angl:6,meta_dict:3,meter:16,method:10,metric:[0,1,2,3,10,12,14,15,19,20],metric_imag:[1,2,17],metric_param:[0,1,10,18],metric_range_graph:1,metric_scor:10,metrics_avg_graph:[0,1],metrics_info_format:[0,1],metrics_nam:10,metrics_to_us:[2,10],might:[18,19],mild:5,mimic:20,min:[10,17,18],minimum:7,mismatch:13,model:[6,7,8,20],modul:[14,15],more:[12,17],most:19,mousepressev:1,mplcanva:10,ms_ssim:5,mse:[1,5,17],mse_imag:17,mssim_kernel_s:5,much:20,multi:[5,6],multipl:[0,15],multipli:7,must:[5,6,7],n:[13,16,19],n_channel:7,name:[1,2,10],navig:16,necessari:20,need:[0,1,6,8,16,17,18,19],net:1,network:[5,7],newer:13,nlpd:5,nlpd_k:5,nlpd_torch:[0,5],nn:[6,7],nois:[5,9],noise_ratio:5,non:[10,17],none:[0,1,2,6,7,10],normal:[7,9,10,17],normalis:[5,7,17],note:[10,18],notebook:[16,17,18,19],nov:7,now:[17,18],np:[5,9,10,18],num_orient:6,num_step:10,num_trans_valu:1,number:[6,7,9,16],numpi:[10,12,18],object:[0,1,5,10,18,20],observ:20,obtain:20,oct:6,octav:6,odd:[9,17],off:18,offer:14,offset:7,often:[13,20],onc:19,one:6,one_over_psnr:5,onli:[6,7,9,10,16,17,19],opencv:[12,13],oper:[7,17,20],optimis:6,option:[2,6,7,12,17,19],order:[1,6,7,12,19],orderpi:6,ordin:12,org:[5,7],orient:6,origin:[6,10],other:[10,12],otherwis:7,our:[14,18],out:[9,10,12],output:[7,8],over:[5,6,7,10,16,17],overridden:6,overse:20,own:[17,18,19],p:6,packag:[13,14,15,17,18],packg:16,pad:[7,8],pair:[5,12],pairwis:19,paper:[5,6],param1:18,param:[1,18],param_group:1,paramet:[2,5,6,7,8,9,10,14,16,18,20],paramt:[10,16],particip:[12,19],particular:12,partit:1,pass:[6,7,17,18],past:16,patch:5,path:[1,2,10,17],pbar_sign:10,pdf:5,peak:5,peak_sign:5,peel:18,peic:17,pepper:9,per:16,perceiv:[12,20],percentag:[9,10],percept:20,perceptu:[5,20],perform:[6,14,20],pick:12,pickl:10,pickle_path:10,pip:13,pivot:1,pixel:9,pkl:10,place:16,platform:13,plethora:20,plot:[1,10,12,19],plot_radar_graph:1,plot_util:[0,15],plu:10,plugin:13,png:18,point:[1,5,10,19],polar:10,posit:7,post:10,practition:[12,14,20],pre:12,precomput:6,premis:20,presenc:20,press:19,pretarin:6,pretrain:[5,6],previou:19,principl:20,print:17,prob:9,probabl:9,procedur:14,process:[6,10,12,17,20],produc:[16,20],profil:20,progress:1,progressbar:1,project:[16,17],properti:[0,2,12,14],proport:9,propos:[5,7],provid:[5,12,14,16,17],psnr:5,psychophys:20,put:18,pypi:13,pyqt6:[0,1,10,12],pyqt:[1,13],pyramid:[0,5,8],pyramid_filt:[5,6],python:[12,13,16],pythontutori:1,pytorch:[5,12],qcloseev:1,qlabel:1,qmainwindow:1,qmouseev:1,qobject:1,qprogressbar:1,qt:13,qtcore:1,qthread:1,qtwidget:1,qualit:[17,20],qualiti:[5,9,12,14,17,20],quantit:20,quick:[12,19],quick_sort:1,quit:1,radar:10,radar_nam:10,radar_plott:10,radial:6,radian:6,rais:[6,7],ranc:10,rang:[1,9,10,16,17,18,20],rate:20,ratio:5,reach:7,read:19,readi:19,real:12,recent:20,recip:6,recommend:[13,16],recreat:20,recurs:12,redo_plot:1,reduc:5,reduct:5,refer:[2,5,10,12,18,20],region:6,regist:6,reinstal:13,remain:20,reparam_offset:7,reparameteris:7,repons:14,repres:7,request_range_work:1,requir:[1,13,16,17,19,20],reset_correlation_data:1,reset_experi:1,reset_slid:1,reset_slider_group:1,residu:6,resiz:[10,12],resize_imag:10,resize_to_longest_sid:10,respect:[12,20],respons:20,restrict_opt:[0,1],result:[1,10,12,14],results_ord:10,return_dict:10,return_imag:[5,17],rgb:10,rgb_bright:[1,10],right:1,robust:5,rotat:[2,6,9,12,16,17],round:14,run:[3,6,7,12,13,14,16],running_an_experi:19,s:[17,18,20],salt:9,salt_and_pepper_nois:9,same:[2,5,6,7,8,18,20],sampl:[5,9],sat:9,satur:9,save:[1,10,16,19],save_experi:1,save_experiment_result:10,save_imag:10,save_json_dict:10,save_obj:10,save_util:[0,15],saved_experi:1,scalar:[5,17],scale:[5,6],scale_factor:[9,10],scatter:10,scatter_plott:10,scenario:[14,20],score:[5,12,18,19],scratch:13,screen:[12,16],script:16,second:[6,20],secondli:14,see:[12,14,17,19],select:[12,14,16,19],self:[1,18],send:10,sent:1,sepcifici:6,serv:20,set:[1,6,14,19],set_checked_menu_from_iter:1,set_image_name_text:1,set_plot_lim:10,set_styl:10,setup:[1,19],setup_experi:1,shape:[7,8,18],shift:9,should:[6,7,13],show:[0,10,12,18,19],show_all_imag:1,shown:[18,19],side:10,sigma:5,signal:[1,5,10],silent:6,similar:[5,17,19,20],simon1995:8,simon1995pyr:6,simoncelli:6,simpl:[0,12,14,15],simpler:10,simplest:20,sinc:[6,17],singl:[10,18],single_trans_dict:1,singular:6,size:[3,6,7,8,9,10,12,19],skimag:9,small:10,smaller:16,smoother:1,so:[1,10,12,13],softwar:20,some:[13,16,17],sort:[1,12,19],sort_list:1,sourc:[0,1,2,3,5,6,7,8,9,10],space:20,spacial:[14,17],spatial:[6,7,8],specif:[7,12,20],specifi:[6,10,17],spider:10,sqrt:7,squar:[5,7,8,9,10,16,18,20],squeez:5,ssim:[5,14,17,20],ssim_imag:17,stack:6,stage:6,stanard:12,standard:12,start:[9,17,18,19],start_experi:1,state:1,steer_matrix:6,steerabl:[6,8],steerablepyramid:6,steerablewavelet:6,still:18,stop:1,stop_flag:10,stopped_range_result:1,storag:12,store:[2,8,17,18],str:[0,5],str_to_len:10,straightforward:12,strictli:5,stride:[7,8],string:10,structur:[5,20],style:1,subband:6,subclass:[1,6],submodul:15,subpackag:15,subtract:5,sudo:13,sum:5,sum_j:7,sure:[0,13,14,18,19],swap_ind:1,system:5,t:6,tab:[1,16],take:[5,6,12,16,18,19],taken:8,task:12,tell:18,tensor:[6,7],test:14,test_datastore_attribut:0,text:10,textur:5,than:[1,6,7,9],theh:16,thei:[2,7,18,19,20],them:[1,6,17,18],thereon:6,theta:6,thi:[6,7,8,10,12,13,16,17,18,19,20],thing:19,thread:[0,15],threshold:9,through:[6,12,14,16,17,19],timescal:12,todo:[0,6,10],toggle_experi:1,too:20,toolbox:14,torch:[6,7],tradit:20,train:[6,7],trainabl:6,tran:[1,10],trans_nam:10,trans_str:[1,10],transform:[0,1,2,3,5,6,7,10,12,14,15,19],transform_funct:10,transform_param:10,transform_valu:10,transformation_nam:10,transformed_imag:2,transit:6,translat:[9,12],treat:7,tree:[16,17,18,19],truthfulli:12,tutori:12,tutorial_1:16,tutorial_2:17,tutorial_3:18,tutorial_4:19,twidth:6,two:[5,6,14,17,20],txt:1,type:[5,6,7,8,9,10],typeerror:[6,7],ubyt:10,ui:[0,2,5,10,14,15,17,19],ui_wrapp:15,unchang:20,under:14,underli:12,understand:[12,14],undistort:12,uninstal:13,union:6,unsort:1,until:19,up:[1,14,17],update_annot:10,update_image_set:1,update_progress:1,update_status_bar:1,upsampl:6,upsample_output:6,us:[1,2,5,6,7,8,9,10,12,13,14,16,17,18,19],usag:0,user:[9,12,14,19],util:[0,2,5,6,15],utilis:20,uv:5,v:1,valero:5,valu:[2,5,6,7,9,10,16,17,18],var_nam:10,var_valu:10,varianc:5,variou:14,version:13,vertic:9,vgg:5,vi:[0,1,2,13,16,17,18,19,20],via:[1,2],video:14,view:[12,14,16,17,18,19],view_correlation_inst:1,virtual:13,visibl:20,visit:14,visual:[5,14],visualis:[12,14],w:6,wa:10,wai:14,want:[17,19],washington:6,wavelet:6,wavelet_transform:6,waves1:17,waves2:17,we:[1,16,17,18,19,20],weight:[6,7],well:[12,13,14],what:[0,18],when:[5,7,10,16,17,19],where:[6,7,20],whether:[5,6,7],which:[2,5,8,10,12,14,20],whole:[10,16,17,18,19],why:20,widget:[0,10,15],widget_nam:1,width:[6,7,8],wiki:5,wikipedia:5,window:1,wise:7,within:[6,16,18],without:14,word:18,work:13,worker:1,world:12,would:16,write:[0,10,14],www:[1,5],x1:6,x2:6,x:[6,7,10],x_label:10,x_shift:9,xcosn:6,xrco:6,y:[7,10,13],y_label:10,y_shift:9,ycosn:6,yirco:6,you:[13,14,16,17,18,19],your:[17,19],yrco:6,zero:[7,17],zoom:[9,10],zoom_imag:9},titles:["IQM_Vis package","IQM_Vis.UI package","IQM_Vis.data_handlers package","IQM_Vis.examples package","IQM_Vis.examples.images package","IQM_Vis.metrics package","IQM_Vis.metrics.NLPD_torch package","IQM_Vis.metrics.NLPD_torch.layers package","IQM_Vis.metrics.NLPD_torch.utils package","IQM_Vis.transformations package","IQM_Vis.utils package","Tutorials","About IQM-Vis","Getting Started","IQM-Vis documentation","IQM_Vis","Tutorial 1: Making the UI","Tutorial 2: Simple Customisation","Tutorial 3: Customisation Details","Tutorial 4: Running an Experiment","IQMs"],titleterms:{"1":16,"2":17,"3":18,"4":19,"function":12,For:20,about:[12,14],ad:16,all:[3,17],an:[14,19,20],analysi:14,bright:16,built:12,choos:20,code:14,common:13,content:[0,1,2,3,4,5,6,7,8,9,10],conv:8,correl:14,custom_widget:1,customis:[17,18],data_api:2,data_api_abstract:2,data_handl:2,dataset:3,detail:18,differ:20,dispali:16,displai:16,dist:3,divisive_normalis:7,document:14,exampl:[3,4],experi:[3,12,16,19],experiment_mod:1,finsih:19,fourier:8,get:[13,14],graph:16,gui_util:10,how:20,human:[12,14],imag:[1,4,16,17],image_util:10,indic:14,info:19,instal:13,iqm:[5,12,14,20],iqm_vi:[0,1,2,3,4,5,6,7,8,9,10,15],issu:13,kodak:3,layer:7,layout:1,load:16,main:1,make:[16,18],max:16,metric:[5,6,7,8,16,17,18],modul:[0,1,2,3,4,5,6,7,8,9,10],multipl:3,nlpd_torch:[6,7,8],offer:12,other:16,own:16,packag:[0,1,2,3,4,5,6,7,8,9,10],percept:[12,14],plot_util:10,post:16,pre:16,process:16,put:17,pyramid:6,pyramid_filt:8,qualit:14,quantit:14,result:19,rgb:16,run:19,save_util:10,screen:19,set:16,simpl:[3,17],size:16,softwar:12,sourc:14,start:[13,14],step:16,submodul:[0,1,2,3,5,6,7,8,9,10],subpackag:[0,3,5,6],tabl:14,task:20,test:13,thread:1,togeth:17,transform:[9,16,17,18],tutori:[11,14,16,17,18,19],type:20,ui:[1,16,18],ui_wrapp:0,util:[1,8,10],vi:[12,14],visualis:19,what:[12,14,20],widget:1,your:[16,20]}})