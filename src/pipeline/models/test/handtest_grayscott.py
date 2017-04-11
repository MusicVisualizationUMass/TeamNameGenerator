from pipeline.models.grayscottmodel import GrayScottModel
import matplotlib.pyplot as plt

def _test_plot(width = 256, height = 256,k = 0.02, ru = 1.7, rv = 0.3,
               f = 2.1, dt = 0.15, pause_time = 0.01):
    '''
    _test_plot() gives a visualization and as such shouldn't be run
    automatically. This should be called explicitly.
    '''
    # TODO: How is this called?
    gs = GrayScottModel(width, height, k, ru, rv, f, dt)
    plt.ion()

    while True:
        gs.increment_time()
        plt.imshow(gs.us) 
        plt.show()
        plt.pause(pause_time)
        print('time =', gs.t)


if __name__ == '__main__':
    _test_plot()

