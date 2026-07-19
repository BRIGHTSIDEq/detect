def precision_recall(tp:int, fp:int, fn:int)->tuple[float,float]:
    """Вычисляет precision и recall."""
    p=tp/(tp+fp) if tp+fp else 0.0; r=tp/(tp+fn) if tp+fn else 0.0
    return p,r
