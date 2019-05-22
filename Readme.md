# 서론
aws, gcp를 비롯한 많은 클라우드 API들이 등장하고 있다. 이들의 등장은 IT 업계에 많은 화두를 던지며 뜨거운 감자로 떠오르고 있다. 그중 인공지능 API는 사용자가 비싼 초기비용을 치를 필요없이 유연한 인프라를 구성할 수 있게 하고, 자체 내장 알고리즘을 제공해 사용자의 시간과 비용을 줄이는 서비스라고 할 수 있다. 그러나 여전히 사용자의 입장에서는 특정 비즈니스 모델(데이터셋)에서 어떤 API가 적용 가능한지, 가능한 것들 중에서는 어떤 API가 최적의 성능을 도출하는지에 대한 인사이트를 얻기가 매우 힘들다. 특히 사용자가 데이터 과학자가 아니라면, 더더욱 이를 확인하는 것은 어려운 작업이 될 것이다. 이를 해결하기 위해, 특정 모델에서 어떤 API가 최적의 성능을 내는지를 확인할 수 있는 패키지를 만들었고, 그 과정에 대한 전체적인 가이드(jupyter notebook 파일)와 API별 가이드를 작성해놓았다. 이 패키지를 통해 사용자가 자신에게 최적화된 API를 선택할 수 있기를 바란다.

# 제약사항
실제로 모든 모델에 대한 모든 API간의 성능비교를 하는 것은 굉장히 많은 양의 작업이기 때문에, 여기에서는 특정 모델에 대한 메이저한 API간의 성능 비교를 순차적으로 진행할 것이다. 비교가 완료된 모델들은 비교된 API와 함께 아래 리스트에 계속 업데이트될 것이다.

# 진행상황

-Anomaly Dectection(Luminol, AWS, Azure)


# 가정
이 패키지는 각 API에 대한 기본적인 지식을 가지고 있는 사용자를 대상으로 한다. 사용자는 비교하고자 하는 각 API의 계정을 반드시 갖고 있어야 하며, 해당 패키지를 이용할 때는 사용자 본인의 계정들을 통해 API 성능을 비교하게 되므로 약간의 비용이 발생하게 된다.

# 성과 수치
금전적 비용, 수행 시간, 정확도 등 수많은 metrics가 존재하지만, 여기에서는 API들이 제공하는 알고리즘의 성과만을 측정할 것이며, 성과 척도는 모델에 따라 다르므로 각 가이드에 기술될 것이다.
