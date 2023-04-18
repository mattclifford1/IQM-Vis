from .IQMs import MAE, MSE, SSIM, MS_SSIM, LPIPS, DISTS

def get_all_metrics():
    ''' Get all available IQMs provided by IQM_Vis '''
    all_metrics = {
        'MSE': MSE(),
        'SSIM': SSIM(),
        'MS_SSIM': MS_SSIM(),
        'DISTS': DISTS(),
        'SSIM': SSIM(),
        'LPIPS': LPIPS(),
        'MAE': MAE(),
    }
    return all_metrics

def get_all_metric_images():
    ''' Get all available IQMs provided by IQM_Vis that return an image '''
    all_metrics = {
    'MSE': MSE(return_image=True),
    'SSIM': SSIM(return_image=True),
    'MAE': MAE(return_image=True),
    # 'MSSIM': MSSIM(return_image=True),
    }
    return all_metrics
