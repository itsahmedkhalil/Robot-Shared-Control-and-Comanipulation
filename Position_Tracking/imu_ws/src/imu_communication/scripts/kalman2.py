import numpy as np

class Kalman():
    def __init__(self, R, Q):
        #self.H = H #traformation matrix from state parameters to measurement domain
        self.Q = Q #covariance/error of process
        self.R = R #covariance/error of measurement
        #self.A = A #state transition matrix
        #self.x_hat_k1_ = x_hat_k1_ #initialize state estimate at time t np.array([0,0,0,0,0,0,1]).T
        #self.P_k1_ = P_k1_ #initialize state covariance at time t
    def predict(self, x_hat_k1_, P_k1_, dT):
        #prediction [x,y,z,x_dot,y_dot,z_dot]
        A = np.array([
            [1,0,0,dT,0,0],
            [0,1,0,0,dT,0],
            [0,0,1,0,0,dT],
            [0,0,0,1,0,0 ],
            [0,0,0,0,1,0 ],
            [0,0,0,0,0,1 ]
                ])
        self.H = np.array([ 
            [0.5*dT**2,         0,         0,    dT,   0,   0],
            [0        , 0.5*dT**2,         0,     0,  dT,   0],
            [0        ,         0, 0.5*dT**2,     0,   0,  dT]
            ])

        x_hat_k = A@x_hat_k1_ #+ B@u
        P_k = A@P_k1_@A.T + self.Q
        return x_hat_k, P_k
    def update(self, x_hat_k, P_k, z_k1_):
        #update
        K = P_k@self.H.T@np.linalg.inv(self.H@P_k@self.H.T + self.R)
        x_k_new = x_hat_k + K@(z_k1_ - self.H@x_hat_k)
        P_k_new = (np.identity(14) - K@self.H)@P_k#(P_k - K@self.H)@P_k
        return x_k_new, P_k_new
        #self.x_hat_k1_ = x_k_new
        #self.P_k1_ = P_k_new
if __name__ == "__main__":
    dT = 0.08
    A = np.array([
                [1,0,0,0,0,0,0,dT,0,0,0,0,0,0],
                [0,1,0,0,0,0,0,0,dT,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0,dT,0,0,0,0],
                [0,0,0,1,0,0,0,0,0,0,dT,0,0,0],
                [0,0,0,0,1,0,0,0,0,0,0,dT,0,0],
                [0,0,0,0,0,1,0,0,0,0,0,0,dT,0],
                [0,0,0,0,0,0,1,0,0,0,0,0,0,dT],
                [0,0,0,0,0,0,0,1,0,0,0,0,0, 0],
                [0,0,0,0,0,0,0,0,1,0,0,0,0, 0],
                [0,0,0,0,0,0,0,0,0,1,0,0,0, 0],
                [0,0,0,0,0,0,0,0,0,0,1,0,0, 0],
                [0,0,0,0,0,0,0,0,0,0,0,1,0, 0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1, 0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0, 1]
                  ])
    H = np.array([
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,1,0,0,0,0,0,0,0]
                ])
    Q = 0.028*np.identity(14)
    R = 0.3*np.identity(7) #0.3
    x_hat_k1_ = np.array([[0,0,0,0,0,0,1,0,0,0,0,0,0,1]]).T # x_t = [T,q,T_dot,q_dot]
    P_k1_ = np.identity(14)
    kalman = Kalman(x_hat_k1_, P_k1_, A, H, R, Q)
    x_hat_k1_, P_k1_ = kalman.main(x_hat_k1_, P_k1_, np.array([0,0,0,0,0,0,1]).T)
    print(x_hat_k1_)
