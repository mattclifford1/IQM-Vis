from .IQMs import (MAE, 
                   MSE, 
                   SSIM, 
                   MS_SSIM, 
                   LPIPS, 
                   DISTS, 
                   NLPD,
                   one_over_PSNR)

def get_all_metrics():
    ''' 
    Get all available IQMs provided by IQM_Vis 
    
    Return:
        - all_metrics (dict)
        '''
    all_metrics = {
        'MSE': MSE(),
        'NLPD': NLPD(),
        '1-SSIM': SSIM(),
        '1-MS_SSIM': MS_SSIM(),
        '1/PSNR': one_over_PSNR(),
        'DISTS': DISTS(),
        'LPIPS': LPIPS(),
        'MAE': MAE(),
    }
    return all_metrics

def get_all_metric_images():
    ''' 
    Get all available IQMs provided by IQM_Vis that return an image 
    
    Return:
        - all_metrics (dict)
    '''
    all_metrics = {
    'MSE': MSE(return_image=True),
    'SSIM': SSIM(return_image=True),
    # 'MS_SSIM': MS_SSIM(return_image=True),
    'MAE': MAE(return_image=True),
    }
    return all_metrics

def get_all_IQM_params():
    ''' 
    Get all available IQMs parameters
    
    Return:
        - all_params (dict)
    '''
    all_params = {
        'sigma': {'min':0.25, 'max':5.25, 'init_value': 1.5},  # for the guassian kernel
        'k1': {'min':0.01, 'max':0.21, 'init_value': 0.01},
        'k2': {'min':0.01, 'max':0.21, 'init_value': 0.03},
        'ssim_kernel_size': {'min':3, 'max':21, 'normalise':'odd', 'init_value': 11},  # ignored if guassian kernel used
        'mssim_kernel_size': {'min':3, 'max':21, 'normalise':'odd', 'init_value': 11},  # ignored if guassian kernel used
    }
    return all_params