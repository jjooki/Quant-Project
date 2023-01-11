# 주식 모멘텀 클래스
class Momentum:
    """Momentum 전략을 관리할 클래스

    Returns:
        pd.DataFrame -> 거래 시그널을 알려주는 df
    """
    
    def __init__(self, rebal_price: pd.DataFrame, 
                lookback_window: int, n_sel: int, 
                long_only: bool=True):
        """초기화 함수

        Args:
            rebal_price (pd.DataFrame): 
                - DataFrame -> price_on_rebal()의 리턴 값. 리밸런싱 날짜의 타켓 상품들 종가 df
            lookback_window (int):
                - int -> 모멘텀(추세)를 확인할 기간 설정
            n_sel (int):
                - int -> 몇 개의 금융상품을 고를지 결정
            long_only (bool, optional): 
                - bool -> 매수만 가능한지 아님 공매도까지 가능한지 결정. Defaults to True.
        """

        self.price = rebal_price
        self.lookback_window = lookback_window
        self.rets = rebal_price.pct_change(self.lookback_window).fillna(0)
        self.n_sel = n_sel

    # 절대 모멘텀 시그널 계산 함수
    def absolute_momentum(self, long_only: bool=True) -> pd.DataFrame:
        """absolute_momentum

        Args:
            long_only (bool, optional): 
                - bool -> 매수만 가능한지 결정. Defaults to True.

        Returns:
            pd.DataFrame -> 투자 시그널 정보를 담고있는 df
        """

        returns = self.rets

        # 롱 시그널
        long_signal = (returns > 0) * 1

        # 숏 시그널
        short_signal = (returns < 0) * -1

        # 토탈 시그널
        if long_only:
            signal = long_signal

        else:
            signal = long_signal + short_signal
        
        return signal
    
    # 상대 모멘텀 시그널 계산 함수
    def relative_momentum(self, long_only: bool=True) -> pd.DataFrame:
        """relative_momentum

        Args:
            long_only (bool, optional): 
                - bool -> 매수만 가능한지 결정. Defaults to True.

        Returns:
            pd.DataFrame -> 투자 시그널 정보를 담고있는 df
        """

        # 수익률
        returns = self.rets

        # 자산 개수 설정
        n_sel = self.n_sel

        # 수익률 순위화
        rank = returns.rank(axis=1, ascending=False)

        # 롱 시그널
        long_signal = (rank <= n_sel) * 1

        # 숏 시그널
        short_signal = (rank >= len(rank.columns) - n_sel + 1) * -1

        # 토탈 시그널
        if long_only:
            signal = long_signal

        else:
            signal = long_signal + short_signal

        return signal
    
    # 듀얼 모멘텀 시그널 계산 함수
    def dual_momentum(self, long_only: bool=True) -> pd.DataFrame:
        """dual_momentum

        Args:
            long_only (bool, optional): 
                - bool -> 매수만 가능한지 결정. Defaults to True.

        Returns:
            pd.DataFrame -> 투자 시그널 정보를 담고있는 df
        """

        # 절대 모멘텀 시그널
        abs_signal = self.absolute_momentum(long_only)

        # 상대 모멘텀 시그널
        rel_signal = self.relative_momentum(long_only)

        # 듀얼 모멘텀 시그널
        signal = (abs_signal == rel_signal) * abs_signal

        return signal

    # def momentum_score(self, long_only: bool=True):
        
    #     price = self.price
    #     score_result = (12*price.pct_change(1)) + (4*price.pct_change(3)) \
    #                                                   + (2*price.pct_change(6)) \
    #                                                   + (1*price.pct_change(12))

    #     score_result = score_result.dropna()

    #     # 2.2 : MOMENTUM SCORE OF CANARY ASSET
    #     canary_signal_series = (score_result[canary_asset] > 0).sum(axis=1)
    #     canary_signal_series
    #     score_result['canary_signal'] = canary_signal_series
    #     score_result

    #     return signal
