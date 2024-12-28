Загрузка модели:

- Загрузка модели происходит с помощью WhisperModel(model_size, device="cpu", compute_type="int8").
- model_size можно установить как 'tiny', 'small', 'medium', 'large-v2'.
- Поскольку вы используете CPU, рекомендуется использовать модели поменьше ('small' или 'tiny') для более быстрой обработки.
- compute_type="int8" оптимизирует вычисления для CPU.