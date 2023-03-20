from .IQMs import MAE, MSE, SSIM, MSSIM, LPIPS, DISTS

def get_all_metrics():
    ''' Get all available IQMs provided by IQM_Vis '''
    all_metrics = {
        'MAE': MAE(),
        'MSE': MSE(),
        'SSIM': SSIM(),
        'DISTS': DISTS(),
        'SSIM': SSIM(),
        'MSSIM': MSSIM(),
        'LPIPS': LPIPS(),
    }
    return all_metrics

def get_all_metric_images():
    ''' Get all available IQMs provided by IQM_Vis that return an image '''
    all_metrics = {
    'MAE': MAE(return_image=True),
    'MSE': MSE(return_image=True),
    'SSIM': SSIM(return_image=True),
    # 'MSSIM': MSSIM(return_image=True),
    }
    return all_metrics
