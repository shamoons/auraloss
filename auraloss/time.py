import torch

class ESRLoss(torch.nn.Module):
    """Error-to-signal ratio loss function module. 
    
    See [Wright & Välimäki, 2019](https://arxiv.org/abs/1911.08922).
    """
    def __init__(self):
        super(ESRLoss).__init__()

    def forward(self, input, target):
        return torch.mean((torch.abs(target-input)**2)/(torch.abs(target)**2))

        import torch

class DCLoss(torch.nn.Module):
    """DC loss function module. 
    
    See [Wright & Välimäki, 2019](https://arxiv.org/abs/1911.08922).
    """
    def __init__(self):
        super(DCLoss, self).__init__()

    def forward(self, input, target):
        return (torch.abs(torch.mean(target-input))**2)/(torch.mean(torch.abs(target)**2))


class LogCoshLoss(torch.nn.Module):
    """Log-cosh loss function module. 
    
    See [Chen et al., 2019](https://openreview.net/forum?id=rkglvsC9Ym).
    """
    def __init__(self, eps=1e-12):
        """Initilize Log cosh loss module
        Args:
            eps (float): Small epsilon value for stablity. Default: 1e-12
        """
        super(LogCoshLoss, self).__init__()
        self.eps = eps

    def forward(self, input, target):
        """Calculate forward propagation.
        Args:
            input (Tensor): Predicted signal (B, #channels, #samples).
            target (Tensor): Groundtruth signal (B, #channels, #samples).
        Returns:
            Tensor: Log cosh loss value.
        """
        return torch.mean(torch.log(torch.cosh(input - target + self.eps)))


class SISDRLoss(torch.nn.Module):
    """Scale-invariant signal-to-distortion ratio loss module.
    
    See [Le Roux et al., 2018](https://arxiv.org/abs/1811.02508)
    """

    def __init__(self):
        """Initilize spectral convergence loss module."""
        super(SISDRLoss, self).__init__()

    def forward(self, input, target):
        """Calculate forward propagation.
        Args:
            input (Tensor): Predicted signal (B, #channels, #samples).
            target (Tensor): Groundtruth signal (B, #channels, #samples).
        Returns:
            Tensor: SI-SDR loss value.
        """
        return None
