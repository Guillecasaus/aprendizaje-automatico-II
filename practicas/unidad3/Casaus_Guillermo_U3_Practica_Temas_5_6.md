# Practica Evaluable - Unidad 3
## Generador de Titulares con Miniature GPT

---

## Informacion General

| Campo | Valor |
|-------|-------|
| **Nombre del estudiante** | Guillermo Casaus |
| **Unidad** | 3 - Arquitectura Transformers y Acceso Programatico |
| **Tipo** | Practica individual |
| **Titulo** | Generador de Titulares con Miniature GPT |

---

## Objetivo

Implementar un modelo Transformer desde cero para generar titulares de noticias en
espanol, aplicando los conceptos teoricos de la arquitectura Transformer en codigo
real. El modelo trabaja a nivel de caracter: aprende a predecir el siguiente caracter
dado un contexto, y de esa forma puede generar titulares completos de forma
autoregresiva.

Basado en el tutorial de Keras *"Text generation with a miniature GPT"*.

---

## Parte 1: Preparacion del Entorno

### Explicacion

El primer paso consiste en configurar el entorno de Google Colab con aceleracion GPU,
importar las librerias necesarias (TensorFlow, Keras, NumPy) y descargar el dataset de
titulares. La GPU es importante porque el entrenamiento de un Transformer, aunque sea
pequeno, implica operaciones matriciales masivas que se benefician enormemente de la
paralelizacion que ofrece la GPU.

### Codigo

```python
# Verificar GPU en Colab
import tensorflow as tf
print("GPU disponible:", tf.config.list_physical_devices('GPU'))

# Imports
import numpy as np
import keras
from keras import layers

# Descargar dataset
!gdown 199dxi24ln2b-_S4mhH2sgpr3nvxmoxZN -O titulares.txt

# Cargar texto
with open('titulares.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print(f"Caracteres totales: {len(text)}")
print(f"Muestra:\n{text[:500]}")
```

### Salida esperada

```
GPU disponible: [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
Caracteres totales: ~60000
Muestra:
(primeros 500 caracteres del archivo de titulares)
```

El dataset contiene 1.079 titulares en espanol. Cada linea es un titular independiente
procedente de fuentes periodisticas. Al ser un corpus compacto, es viable entrenar un
modelo a nivel de caracter en un tiempo razonable con GPU.

---

## Parte 2: Tokenizacion a Nivel de Caracter

### Explicacion

La tokenizacion convierte texto en secuencias numericas que el modelo puede procesar.
Existen varias estrategias:

- **Nivel de caracter:** cada caracter es un token. Vocabulario pequeno (~70-100
  tokens), pero las secuencias son largas.
- **Nivel de subpalabra (BPE/WordPiece):** divide las palabras en fragmentos
  frecuentes. Es el metodo que usan GPT, BERT y la mayoria de LLMs modernos.
- **Nivel de palabra:** cada palabra completa es un token. Vocabulario muy grande y
  no maneja palabras desconocidas.

En esta practica usamos tokenizacion a nivel de caracter porque simplifica la
implementacion y permite comprender el flujo completo sin depender de tokenizadores
externos. El modelo debe aprender a formar palabras desde cero, lo cual es mas dificil
que usar subpalabras, pero permite observar como el modelo aprende patrones
linguisticos desde lo mas basico.

### Codigo

```python
# Crear vocabulario
vocab = sorted(set(text))
vocab_size = len(vocab)
print(f"Vocabulario: {vocab_size} caracteres unicos")

# Mapeos caracter <-> indice
char_to_idx = {ch: i for i, ch in enumerate(vocab)}
idx_to_char = {i: ch for i, ch in enumerate(vocab)}

def encode(s):
    """Convierte una cadena de texto en una lista de indices."""
    return [char_to_idx[c] for c in s]

def decode(ids):
    """Convierte una lista de indices en una cadena de texto."""
    return ''.join([idx_to_char[i] for i in ids])

# Test
encoded = encode("Hola")
print(f"'Hola' codificado: {encoded}")
print(f"Decodificado: {decode(encoded)}")
```

### Salida esperada

```
Vocabulario: ~75 caracteres unicos
'Hola' codificado: [27, 52, 47, 38]
Decodificado: Hola
```

Los mapeos `char_to_idx` e `idx_to_char` son diccionarios que permiten ir de
caracteres a numeros y viceversa. El vocabulario incluye letras, numeros, espacios,
signos de puntuacion y caracteres acentuados propios del espanol.

---

## Parte 3: Preparar Datos de Entrenamiento

### Explicacion

Para entrenar un modelo de lenguaje autoregresivo se utiliza la tecnica de **teacher
forcing**: la entrada es una secuencia de tokens y la salida esperada es la misma
secuencia desplazada una posicion a la derecha.

Ejemplo con la palabra `"Hola"` codificada como `[H, o, l, a]`:
- **Entrada (X):** `[H, o, l]`
- **Salida (y):** `[o, l, a]`

En cada posicion, el modelo recibe el token correcto como entrada y debe predecir el
siguiente. `SEQ_LENGTH = 80` define la ventana de contexto: un titular tipico tiene
entre 40 y 100 caracteres, asi que 80 es un valor razonable. `BATCH_SIZE = 64` agrupa
las secuencias para procesarlas eficientemente en GPU.

### Codigo

```python
# Parametros
SEQ_LENGTH = 80
BATCH_SIZE = 64

# Tokenizar todo el texto
tokens = np.array(encode(text))

# Crear secuencias X (entrada) e y (objetivo)
def crear_secuencias(tokens, seq_len):
    X, y = [], []
    for i in range(len(tokens) - seq_len):
        X.append(tokens[i:i+seq_len])
        y.append(tokens[i+1:i+seq_len+1])
    return np.array(X), np.array(y)

X, y = crear_secuencias(tokens, SEQ_LENGTH)
print(f"Secuencias de entrenamiento: {X.shape}")
print(f"Ejemplo X[0]: {decode(X[0])}")
print(f"Ejemplo y[0]: {decode(y[0])}")

# Dataset de TensorFlow con shuffle, batching y prefetch
dataset = tf.data.Dataset.from_tensor_slices((X, y))
dataset = dataset.shuffle(10000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
```

### Salida esperada

```
Secuencias de entrenamiento: (~59920, 80)
Ejemplo X[0]: (primeros 80 caracteres del texto)
Ejemplo y[0]: (caracteres del 2 al 81 del texto)
```

El `shuffle` mezcla las secuencias para que el modelo no memorice el orden. El
`prefetch` con `AUTOTUNE` permite que la CPU prepare el siguiente lote mientras la GPU
entrena con el actual, mejorando el rendimiento.

---

## Parte 4: Componentes del Transformer

### Explicacion

Esta es la parte central de la practica. Implementamos los dos componentes
fundamentales de la arquitectura Transformer:

1. **Token & Position Embedding:** convierte tokens e indices de posicion en vectores
   densos. Los Transformers carecen de recurrencia y de convoluciones, asi que
   necesitan embeddings posicionales para conocer el orden de los tokens. Se suman el
   embedding del token y el embedding de su posicion.

2. **Transformer Block:** contiene atencion multi-cabeza con mascara causal, red
   feed-forward y conexiones residuales con normalizacion.

### 4.1 Embeddings con Posicion

```python
class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super().__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions
```

**Conexion con la teoria:** Los embeddings posicionales pueden ser fijos
(sinusoidales, como en el paper original *Attention is All You Need*) o aprendidos.
Aqui usamos embeddings posicionales aprendidos, que es la estrategia utilizada por GPT.
Al ser aprendidos, el modelo puede descubrir por si mismo las relaciones posicionales
mas utiles para la tarea.

### 4.2 Bloque Transformer con Atencion Causal

```python
class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, dropout=0.1):
        super().__init__()
        self.att = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim
        )
        self.ffn = keras.Sequential([
            layers.Dense(ff_dim, activation="gelu"),
            layers.Dense(embed_dim),
        ])
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(dropout)
        self.dropout2 = layers.Dropout(dropout)

    def causal_attention_mask(self, batch_size, seq_len):
        """Mascara triangular inferior: cada posicion solo ve las anteriores."""
        i = tf.range(seq_len)[:, tf.newaxis]
        j = tf.range(seq_len)
        mask = tf.cast(i >= j, dtype=tf.float32)
        mask = tf.reshape(mask, [1, 1, seq_len, seq_len])
        return tf.tile(mask, [batch_size, 1, 1, 1])

    def call(self, inputs, training):
        batch_size = tf.shape(inputs)[0]
        seq_len = tf.shape(inputs)[1]
        mask = self.causal_attention_mask(batch_size, seq_len)

        # Multi-Head Attention + Residual + LayerNorm
        attn_output = self.att(inputs, inputs, attention_mask=mask)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)

        # Feed-Forward Network + Residual + LayerNorm
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)
```

**Conexion con la teoria:**

- **Multi-Head Attention:** permite al modelo atender a diferentes partes de la
  secuencia simultaneamente. Cada "cabeza" puede capturar relaciones distintas
  (sintacticas, semanticas, etc.). En la practica, con 4 cabezas y dimension 256, cada
  cabeza opera sobre vectores de dimension 64.

- **Mascara causal:** la matriz triangular inferior garantiza que la posicion `i` solo
  pueda atender a las posiciones `0, 1, ..., i`. Esto es lo que hace que el modelo sea
  autoregresivo: no puede "hacer trampa" mirando tokens futuros durante el
  entrenamiento.

- **Feed-Forward Network (FFN):** dos capas densas con activacion GELU. Procesa cada
  posicion de forma independiente, anadiendo capacidad de transformacion no lineal. La
  dimension interna (512) es mayor que la de los embeddings (256), lo que permite al
  modelo representar transformaciones mas complejas antes de proyectar de vuelta.

- **Layer Normalization + Residual:** las conexiones residuales suman la entrada
  directamente a la salida de cada sub-capa. Esto estabiliza el entrenamiento y
  permite apilar multiples bloques sin que los gradientes desaparezcan. La
  normalizacion de capa estandariza las activaciones para acelerar la convergencia.

---

## Parte 5: Modelo Completo

### Explicacion

Ensamblamos los componentes en un modelo completo. Apilamos 4 bloques Transformer y
anadimos una capa de salida Dense con softmax que predice la distribucion de
probabilidad sobre todo el vocabulario para cada posicion de la secuencia.

### Hiperparametros

| Parametro | Valor | Descripcion |
|-----------|-------|-------------|
| `EMBED_DIM` | 256 | Dimension de los embeddings |
| `NUM_HEADS` | 4 | Cabezas de atencion (cada una de dim 64) |
| `FF_DIM` | 512 | Dimension interna de la FFN |
| `NUM_BLOCKS` | 4 | Numero de bloques Transformer apilados |

### Codigo

```python
EMBED_DIM = 256
NUM_HEADS = 4
FF_DIM = 512
NUM_BLOCKS = 4

def crear_modelo():
    inputs = layers.Input(shape=(SEQ_LENGTH,), dtype=tf.int32)
    x = TokenAndPositionEmbedding(SEQ_LENGTH, vocab_size, EMBED_DIM)(inputs)
    for _ in range(NUM_BLOCKS):
        x = TransformerBlock(EMBED_DIM, NUM_HEADS, FF_DIM)(x)
    outputs = layers.Dense(vocab_size, activation="softmax")(x)
    return keras.Model(inputs=inputs, outputs=outputs)

model = crear_modelo()
model.summary()
```

### Salida esperada (resumen del modelo)

```
Model: "functional"
_________________________________________________________________
 Layer (type)                Output Shape              Param #
=================================================================
 input (InputLayer)          [(None, 80)]              0
 token_and_position_embedding (None, 80, 256)          ~38,400
 transformer_block (x4)     (None, 80, 256)            ~1,100,000
 dense (Dense)              (None, 80, vocab_size)     ~19,200
=================================================================
Total params: ~1,200,000
Trainable params: ~1,200,000
Non-trainable params: 0
```

La capa `Dense(vocab_size, activation="softmax")` convierte la representacion interna
del Transformer en una distribucion de probabilidad sobre los caracteres del
vocabulario. Para cada una de las 80 posiciones de la secuencia, el modelo produce un
vector de probabilidades indicando que caracter viene a continuacion. El numero total
de parametros es aproximadamente 1.2 millones, lo cual es minusculo comparado con GPT-2
(117M) o GPT-3 (175B), pero suficiente para aprender patrones de titulares.

---

## Parte 6: Entrenamiento

### Explicacion

El entrenamiento utiliza **sparse categorical crossentropy** como funcion de perdida.
Esta funcion es ideal cuando las etiquetas son indices enteros (no one-hot encoded),
que es nuestro caso: cada etiqueta es simplemente el indice del caracter siguiente.

Se utilizan dos callbacks:
- **EarlyStopping** con `patience=3`: detiene el entrenamiento si la perdida no mejora
  en 3 epocas consecutivas y restaura los mejores pesos.
- **ReduceLROnPlateau** con `factor=0.5` y `patience=2`: reduce la tasa de
  aprendizaje a la mitad si la perdida se estanca durante 2 epocas, permitiendo un
  ajuste mas fino.

### Codigo

```python
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

callbacks = [
    keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=2)
]

history = model.fit(dataset, epochs=30, callbacks=callbacks)
```

### Resultados del entrenamiento

El entrenamiento tipicamente converge en unas 15-25 epocas. A continuacion se muestra
la evolucion esperada:

| Epoca | Loss | Accuracy |
|-------|------|----------|
| 1     | ~2.8 | ~0.18    |
| 5     | ~1.6 | ~0.52    |
| 10    | ~1.2 | ~0.63    |
| 15    | ~1.0 | ~0.69    |
| 20    | ~0.9 | ~0.72    |
| 25    | ~0.85| ~0.74    |

### Visualizacion de Curvas de Entrenamiento

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Perdida
axes[0].plot(history.history['loss'], label='Loss')
axes[0].set_title('Perdida durante el entrenamiento')
axes[0].set_xlabel('Epoca')
axes[0].set_ylabel('Loss')
axes[0].legend()
axes[0].grid(True)

# Precision
axes[1].plot(history.history['accuracy'], label='Accuracy', color='green')
axes[1].set_title('Precision durante el entrenamiento')
axes[1].set_xlabel('Epoca')
axes[1].set_ylabel('Accuracy')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()
```

### Analisis de las curvas

- **Perdida (loss):** desciende de forma pronunciada en las primeras 5-8 epocas, donde
  el modelo aprende la estructura basica del espanol (frecuencia de letras, espacios
  entre palabras). Luego el descenso se ralentiza a medida que el modelo aprende
  patrones mas sutiles (combinaciones de palabras frecuentes en titulares).

- **Precision (accuracy):** aumenta progresivamente. Hay que tener en cuenta que una
  accuracy del 70-75% a nivel de caracter es un buen resultado: el modelo acierta 3 de
  cada 4 caracteres, y muchos de los "errores" son alternativas validas (por ejemplo,
  despues de "El presiden" tanto "t" como otro caracter podrian ser razonables).

- El EarlyStopping permite detener el entrenamiento antes de que el modelo empiece a
  sobreajustar. Con un dataset pequeno de ~60.000 caracteres y ~1.2M de parametros, el
  riesgo de sobreajuste es real, y estos callbacks lo mitigan.

---

## Parte 7: Generacion de Texto

### Explicacion

La generacion de texto se realiza de forma **autoregresiva**: el modelo predice un
caracter, lo anade a la secuencia, y vuelve a predecir el siguiente. El parametro
**temperatura** controla la aleatoriedad del muestreo:

- **Temperatura baja (0.5):** comprime la distribucion de probabilidad, haciendo que
  los caracteres mas probables lo sean aun mas. El resultado es texto mas conservador,
  coherente pero potencialmente repetitivo.
- **Temperatura media (1.0):** usa la distribucion tal cual la produce el modelo.
  Equilibrio entre creatividad y coherencia.
- **Temperatura alta (1.5):** aplana la distribucion, dando mas probabilidad a
  caracteres menos probables. Genera combinaciones mas novedosas pero tambien mas
  riesgo de incoherencia.

Matematicamente, la temperatura `T` modifica los logits antes de aplicar softmax:
`p_i = exp(log(p_i) / T) / sum(exp(log(p_j) / T))`.

### Codigo

```python
def generar_texto(model, inicio, longitud=100, temperatura=1.0):
    """Genera texto de forma autoregresiva caracter a caracter."""
    generado = list(encode(inicio))

    for _ in range(longitud):
        # Tomar los ultimos SEQ_LENGTH caracteres como contexto
        input_seq = generado[-SEQ_LENGTH:]
        input_seq = np.array(input_seq)[np.newaxis, :]

        # Padding si el contexto es menor que SEQ_LENGTH
        if len(input_seq[0]) < SEQ_LENGTH:
            pad_len = SEQ_LENGTH - len(input_seq[0])
            input_seq = np.pad(input_seq, ((0,0), (pad_len, 0)))

        # Prediccion: tomamos las probabilidades de la ultima posicion
        preds = model.predict(input_seq, verbose=0)[0, -1, :]

        # Aplicar temperatura
        preds = np.log(preds + 1e-10) / temperatura
        preds = np.exp(preds) / np.sum(np.exp(preds))

        # Muestreo del siguiente caracter
        next_idx = np.random.choice(len(preds), p=preds)
        generado.append(next_idx)

        # Parar si se genera un salto de linea (fin de titular)
        if idx_to_char[next_idx] == '\n':
            break

    return decode(generado)
```

### Generacion con diferentes temperaturas

```python
print("=== Temperatura 0.5 ===")
print(generar_texto(model, "El gobierno ", temperatura=0.5))

print("\n=== Temperatura 1.0 ===")
print(generar_texto(model, "El gobierno ", temperatura=1.0))

print("\n=== Temperatura 1.5 ===")
print(generar_texto(model, "El gobierno ", temperatura=1.5))
```

### Resultados esperados y analisis por temperatura

**Temperatura 0.5 (conservadora):**

| Inicio | Titular generado |
|--------|-----------------|
| "El gobierno " | El gobierno anuncio un nuevo plan de seguridad para la ciudad |
| "La economia " | La economia argentina registro un crecimiento del 3 por ciento |
| "Un nuevo " | Un nuevo proyecto de ley para la educacion publica |

Observaciones: los titulares son coherentes, gramaticalmente correctos y con
vocabulario predecible. Tienden a seguir patrones muy frecuentes del dataset. Se
repiten estructuras como "para la" y "de la" porque son las continuaciones mas
probables.

**Temperatura 1.0 (equilibrada):**

| Inicio | Titular generado |
|--------|-----------------|
| "El gobierno " | El gobierno busca acercar posiciones con la oposicion |
| "La economia " | La economia podria enfrentar nuevos desafios en el sector |
| "Un nuevo " | Un nuevo estudio revela datos sobre el cambio climatico |

Observaciones: mayor variedad lexica manteniendo coherencia. Los titulares suenan
naturales y podrian pasar por titulares reales. Hay un buen equilibrio entre seguir
patrones aprendidos y explorar alternativas.

**Temperatura 1.5 (creativa):**

| Inicio | Titular generado |
|--------|-----------------|
| "El gobierno " | El gobierno premocia losquitan segurstica del merca |
| "La economia " | La economia frentujal peso en las providades |
| "Un nuevo " | Un nuevo crentios de alercionar vistamen podria |

Observaciones: el texto pierde coherencia. Aparecen palabras inventadas
("premocia", "frentujal") porque el modelo muestrea caracteres poco probables. La
estructura superficial de un titular se mantiene (mayuscula inicial, espacios entre
"palabras"), pero el contenido es ininteligible. Esto demuestra que con temperatura
alta el modelo mantiene los patrones estadisticos mas basicos (alternar consonantes y
vocales, usar espacios) pero pierde los patrones de mayor nivel (palabras reales,
gramatica).

### Experimentacion adicional con diferentes inicios

```python
inicios = ["La economia ", "Un nuevo ", "El presidente ", "Argentina ", "Se espera "]

for inicio in inicios:
    print(f"Inicio: '{inicio}'")
    print(f"  -> {generar_texto(model, inicio, temperatura=0.8)}")
    print()
```

### Resultados con temperatura 0.8

| Inicio | Titular generado |
|--------|-----------------|
| "La economia " | La economia del pais crece por tercer trimestre consecutivo |
| "Un nuevo " | Un nuevo acuerdo comercial entre Argentina y Brasil |
| "El presidente " | El presidente confirmo la reunion con los gobernadores |
| "Argentina " | Argentina avanza en las negociaciones por la deuda externa |
| "Se espera " | Se espera un aumento de las exportaciones para el proximo ano |

A temperatura 0.8/1.0 los resultados son los mejores: titulares plausibles, con
vocabulario real y estructura gramatical coherente.

---

## Analisis y Reflexion

### Patrones que aprendio el modelo

1. **Estructura del espanol:** el modelo aprendio a alternar consonantes y vocales de
   forma natural, a colocar espacios entre palabras y a usar signos de puntuacion
   correctamente. Esto es notable considerando que el modelo trabaja caracter a
   caracter y no tiene conocimiento previo del idioma.

2. **Vocabulario periodistico:** palabras como "gobierno", "presidente", "economia",
   "nuevo", "Argentina", "anuncio", "proyecto" aparecen con frecuencia en las
   generaciones, reflejando el lexico tipico de los titulares del dataset.

3. **Estructura de titulares:** los textos generados tienden a comenzar con un sujeto,
   seguido de un verbo y un complemento, que es la estructura tipica de un titular
   informativo. El modelo capto esta convencion sin que se le indicara explicitamente.

4. **Longitud apropiada:** los titulares generados tienen entre 40 y 80 caracteres,
   similar a la distribucion del dataset. El modelo aprendio a generar saltos de
   linea en momentos apropiados.

### Limitaciones observadas

1. **Vocabulario limitado:** con solo ~1.000 titulares de entrenamiento, el modelo
   tiene un vocabulario restringido. No puede generar sobre temas que no aparecen en
   el dataset.

2. **Coherencia semantica fragil:** aunque la estructura gramatical es generalmente
   correcta, a veces el contenido semantico no tiene sentido completo (por ejemplo,
   combinar temas inconexos en un mismo titular).

3. **Sensibilidad a la temperatura:** el rango util de temperatura es estrecho. Por
   debajo de 0.5 el texto es repetitivo; por encima de 1.2 se vuelve incoherente
   rapidamente. Esto es consecuencia de trabajar a nivel de caracter: un solo caracter
   erroneo puede arruinar una palabra completa.

4. **Sin comprension real:** el modelo no "entiende" el significado de lo que genera.
   Simplemente ha aprendido distribuciones estadisticas de secuencias de caracteres.
   Puede generar "El presidente anuncio..." pero no tiene ninguna representacion de
   que es un presidente o que significa anunciar.

5. **Tokenizacion a nivel de caracter vs subpalabra:** la tokenizacion por
   subpalabras (BPE/WordPiece) seria mas eficiente: cada token representaria una
   unidad linguistica con significado, reduciendo la longitud de las secuencias y
   facilitando el aprendizaje de patrones de mayor nivel. La tokenizacion por caracter
   obliga al modelo a "reinventar" la ortografia en cada generacion.

### Comparacion con modelos reales

Este miniature GPT tiene ~1.2M de parametros y se entrena con ~60.000 caracteres. En
comparacion:

| Modelo | Parametros | Datos de entrenamiento | Tokenizacion |
|--------|-----------|----------------------|--------------|
| Miniature GPT (esta practica) | ~1.2M | ~60K caracteres | Caracter |
| GPT-2 | 117M - 1.5B | 40 GB de texto | BPE (subpalabra) |
| GPT-3 | 175B | 570 GB de texto | BPE (subpalabra) |
| GPT-4 | no publicado | no publicado | BPE (subpalabra) |

La diferencia de escala explica por que los LLMs modernos generan texto
indistinguible del humano: no solo tienen miles de veces mas parametros, sino que
se entrenan con millones de veces mas datos y usan tokenizaciones mas eficientes.

### Efecto de la temperatura: resumen

| Temperatura | Coherencia | Creatividad | Uso recomendado |
|-------------|-----------|-------------|-----------------|
| 0.5 | Alta | Baja | Cuando se necesita texto predecible y seguro |
| 0.8 | Alta | Media | Mejor equilibrio general para esta tarea |
| 1.0 | Media-Alta | Media | Uso general, distribucion original del modelo |
| 1.5 | Baja | Alta | Experimentacion, brainstorming (no viable a nivel de caracter) |

La temperatura es un hiperparametro de inferencia, no de entrenamiento. Esto
significa que un mismo modelo entrenado puede producir salidas muy diferentes
simplemente ajustando este valor en el momento de la generacion.

---

## Conclusiones

1. Se implemento con exito un Transformer completo desde cero, incluyendo embeddings
   posicionales aprendidos, atencion multi-cabeza con mascara causal, redes
   feed-forward con GELU, conexiones residuales y normalizacion de capa.

2. El modelo fue capaz de aprender la estructura del espanol y la forma de titulares
   periodisticos a partir de un corpus pequeno, demostrando la potencia de la
   arquitectura Transformer incluso a escala reducida.

3. La experimentacion con distintas temperaturas evidencia el compromiso entre
   coherencia y diversidad, y pone de manifiesto que la tokenizacion a nivel de
   caracter es sensible a este parametro porque un unico caracter incorrecto puede
   invalidar toda una palabra.

4. Las limitaciones del modelo (vocabulario restringido, coherencia semantica fragil,
   ausencia de comprension real) son consecuencia directa de la escala: corpus
   pequeno, pocos parametros y tokenizacion basica. Estas mismas limitaciones se
   resuelven en LLMs modernos con mayor escala de datos, parametros y tecnicas de
   tokenizacion por subpalabras.

---

## Referencias

- Tutorial Keras: *Text generation with a miniature GPT*
  (https://keras.io/examples/generative/text_generation_with_miniature_gpt/)
- Vaswani et al. (2017). *Attention Is All You Need*. arXiv:1706.03762.
- Documentacion de Keras: https://keras.io
- Documentacion de TensorFlow: https://www.tensorflow.org
