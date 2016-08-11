from banditvis.manager import run
import time

if __name__ == "__main__":
    start_time = time.clock()

    run()

    # print runtime
    stop_time = time.clock()
    m, s = divmod(stop_time - start_time, 60)
    h, m = divmod(m, 60)
    print ("\nRuntime: {:d}h {:d}m {:.3f}s".format(int(h), int(m), s))