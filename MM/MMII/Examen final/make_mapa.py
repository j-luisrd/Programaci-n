import numpy as np
import matplotlib.pyplot as plt

# Creamos un array con ceros, los cuales serán substituidos
# con el modelo de brillo
a = np.zeros([100,100])
x = np.arange(100)
y = np.arange(100)
# yy,xx son vectores que, emparejados, representan todas las posibles
# coordenadas (x,y) de cada pixel en el mapa
yy,xx = np.meshgrid(x,y)
# definimos la posición central del array en pixels
xc,yc = 49.5,49.5
# calculamos la distancia desde el origen hasta cada pixel
R = np.sqrt((xx-xc)**2 + (yy-yc)**2)
# graficamos el mapa de radios R para ver si es lo esperado
plt.imshow(R)
plt.colorbar()
plt.show()

# ahora creamos un modelo de masa basado en un perfil exponencial
masa = 100*np.exp(-R/10)

# graficamos para confirmar
plt.imshow(masa)
plt.colorbar()
plt.show()

# Finalmente, perturbamos el mapa para que en un principio
# no sea perfectamente axisimétrico
masa = masa * np.random.normal(loc=1,scale=0.1,size=masa.shape)

# graficamos para confirmar
plt.imshow(masa)
plt.colorbar()
plt.show()


np.savetxt("mapa.txt",masa)
