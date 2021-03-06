from caffe.proto import caffe_pb2
import tempfile

def make_solver(snapshot_dir, train_net_path, test_net_path, base_lr=0.0001, boost=1):
    s = caffe_pb2.SolverParameter()

    # Specify locations of the train and (maybe) test networks.
    s.train_net = train_net_path
    if test_net_path != '':
        s.test_initialization=False
        s.test_net.append(test_net_path)
        # Don't use caffe testing, we write our own tests in training script
        s.test_interval = 99999999 
        s.test_iter.append(100000000) 

    # The number of iterations over which to average the gradient.
    # Effectively boosts the training batch size by the given factor, without
    # affecting memory utilization.
    s.iter_size = boost
    
    s.solver_type = caffe_pb2.SolverParameter.SGD 
    s.base_lr = base_lr
    s.momentum = 0.9 
    s.weight_decay = 5e-4
    s.display = 100 # display training loss every 100 iters
    s.solver_mode = caffe_pb2.SolverParameter.GPU
    s.debug_info = False
    # Write the solver to a temporary file and return its filename.
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(str(s))
        return f.name

