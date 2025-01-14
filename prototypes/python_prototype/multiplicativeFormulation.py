##Author: Ilia Rushkin, VPAL Research, Harvard University, Cambridge, MA, USA

import numpy as np
import pandas as pd

from fakeInitials import initialize_variables
from derivedData import calculate_derived_data
from empiricalEstimation import estimate


class MultiplicativeFormulation(object):
    def __init__(self, **kwargs):
        initialize_variables(self, **kwargs)
        calculate_derived_data(self)

    def mapUser(self, user_id):
        """
        This function maps the user_id to the user index used by other functions, and also adds new users
        SYNCHRONIZATION IS IMPORTANT
        """
        # global users

        try:
            u = np.where(self.users == user_id)[0][0]
        except:
            """
            Add a new user
            """
            # global n_users, last_seen, m_L, m_exposure, m_unseen, m_correctness, m_timestamp
            n_users = len(self.users)
            u = n_users
            # n_users+=1
            self.users = np.append(self.users, user_id)
            self.last_seen = np.append(self.last_seen, -1)
            self.m_L = np.vstack((self.m_L, L_i))
            self.m_exposure = np.vstack((self.m_exposure, row_exposure))
            self.m_unseen = np.vstack((self.m_unseen, row_unseen))
        #        m_correctness=np.vstack((m_correctness,row_correctness))
        #        m_timestamp=np.vstack((m_timestamp,row_timestamp))

        return u

    def mapItem(self, item_id):

        item = np.where(self.items == item_id)[0][0]

        return item

    def bayesUpdate(self, u, item, score=1.0, time=0, attempts="all"):

        # This function updates the user mastery and record of interactions that will be needed for recommendation and estimation of the BKT

        # global m_x0_mult, m_x1_0_mult, m_L, m_trans, last_seen, m_unseen, transactions, m_exposure, m_tagging, epsilon, inv_epsilon

        self.last_seen[u] = item
        #  m_correctness[u,item]=score
        #  m_timestamp[u,item]=time
        if self.m_unseen[u, item]:
            self.m_unseen[u, item] = False
            self.m_exposure[u,] += self.m_tagging[
                item,
            ]
            self.m_confidence[u,] += self.m_k[
                item,
            ]

            if attempts == "first":
                ##Record the transaction by appending a new row to the data frame "transactions":
                self.transactions = self.transactions.append(
                    pd.DataFrame(
                        [[u, item, time, score]],
                        columns=["user_id", "problem_id", "time", "score"],
                    ),
                    ignore_index=True,
                )
                ##The increment of odds due to evidence of the problem, but before the transfer
                x = self.m_x0_mult[item,] * np.power(
                    self.m_x1_0_mult[
                        item,
                    ],
                    score,
                )
                L = (
                    self.m_L[
                        u,
                    ]
                    * x
                )
                ##Add the transferred knowledge
                L += self.m_trans[
                    item,
                ] * (L + 1)

        if attempts != "first":
            ##Record the transaction by appending a new row to the data frame "transactions":
            self.transactions = self.transactions.append(
                pd.DataFrame(
                    [[u, item, time, score]],
                    columns=["user_id", "problem_id", "time", "score"],
                ),
                ignore_index=True,
            )
            ##The increment of odds due to evidence of the problem, but before the transfer
            x = self.m_x0_mult[item,] * np.power(
                self.m_x1_0_mult[
                    item,
                ],
                score,
            )
            L = (
                self.m_L[
                    u,
                ]
                * x
            )
            ##Add the transferred knowledge
            L += self.m_trans[
                item,
            ] * (L + 1)

        L[np.where(np.isposinf(L))] = self.inv_epsilon
        L[np.where(L == 0.0)] = self.epsilon

        self.m_L[
            u,
        ] = L

        # m_L[u,]+=trans[item,]*(L+1)

        # return{'L':L, 'x':x}

    # This function calculates the probability of correctness on a problem, as a prediction based on student's current mastery.
    def predictCorrectness(self, u, item):

        # global m_L, m_p_slip, m_p_guess

        L = self.m_L[
            u,
        ]
        p_slip = self.m_p_slip[
            item,
        ]
        p_guess = self.m_p_guess[
            item,
        ]

        x = (L * (1.0 - p_slip) + p_guess) / (L * p_slip + 1.0 - p_guess)
        ##Odds by LO
        x = np.prod(x)  ##Total odds

        p = x / (1 + x)  ##Convert odds to probability
        if np.isnan(p) or np.isinf(p):
            p = 1.0

        return p

    ##This function returns the id of the next recommended problem in an adaptive module. If none is recommended (list of problems exhausted or the user has reached mastery) it returns None.
    def recommend(self, u, module=0, stopOnMastery=False, normalize=False):

        # global m_L, L_star, m_w, m_unseen, m_k, r_star, last_seen, m_difficulty, W_r, W_d, W_p, W_c, scope

        # Subset to the unseen problems from the relevant scope
        # ind_unseen=np.where(m_unseen[u,] & ((scope==module)|(scope==0)))[0]
        ind_unseen = np.where(
            self.m_unseen[
                u,
            ]
            & (self.scope[:, module])
        )[0]
        L = np.log(
            self.m_L[
                u,
            ]
        )
        if stopOnMastery:
            m_k_unseen = self.m_k[
                ind_unseen,
            ]
            R = np.dot(m_k_unseen, np.maximum((self.L_star - L), 0))
            ind_unseen = ind_unseen[R != 0.0]

        N = len(ind_unseen)

        if N == 0:  ##This means we ran out of problems, so we stop
            next_item = None

        else:
            # L=np.log(m_L[u,])

            # Calculate the user readiness for LOs

            m_r = np.dot(np.minimum(L - self.L_star, 0), self.m_w)
            m_k_unseen = self.m_k[
                ind_unseen,
            ]
            P = np.dot(m_k_unseen, np.minimum((m_r + self.r_star), 0))
            R = np.dot(m_k_unseen, np.maximum((self.L_star - L), 0))

            if self.last_seen[u] < 0:
                C = np.repeat(0.0, N)
            else:
                C = np.sqrt(
                    np.dot(
                        m_k_unseen,
                        self.m_k[
                            self.last_seen[u],
                        ],
                    )
                )

            # A=0.0
            d_temp = self.m_difficulty[:, ind_unseen]
            L_temp = np.tile(L, (N, 1)).transpose()
            D = -np.diag(np.dot(m_k_unseen, np.abs(L_temp - d_temp)))

            # if stopOnMastery and sum(D)==0: ##This means the user has reached threshold mastery in all LOs relevant to the problems in the homework, so we stop
            next_item = None
            # else:

            if normalize:
                temp = D.max() - D.min()
                if temp != 0.0:
                    D = D / temp
                temp = R.max() - R.min()
                if temp != 0.0:
                    R = R / temp
                temp = P.max() - P.min()
                if temp != 0.0:
                    P = P / temp
                temp = C.max() - C.min()
                if temp != 0.0:
                    C = C / temp

            next_item = ind_unseen[
                np.argmax(self.W_p * P + self.W_r * R + self.W_d * D + self.W_c * C)
            ]

        return next_item

    def updateModel(self):

        # global eta, M, L_i, m_exposure, m_L, m_L_i, m_trans, m_guess, m_slip
        est = estimate(self, self.eta, self.M)

        self.L_i = 1.0 * est["L_i"]
        self.m_L_i = np.tile(self.L_i, (self.m_L.shape[0], 1))

        ind_pristine = np.where(self.m_exposure == 0.0)
        self.m_L[ind_pristine] = self.m_L_i[ind_pristine]
        m_trans = 1.0 * est["trans"]
        m_guess = 1.0 * est["guess"]
        m_slip = 1.0 * est["slip"]
        # execfile('derivedData.py')
        calculate_derived_data(self)
