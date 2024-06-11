
def funcion_densidad_pascal(x, r_pascal, p_pascal):
    # Calcula la combinación binomial
    binomial_coefficient = math.factorial(
        x + r_pascal - 1) / (math.factorial(x) * math.factorial(r_pascal - 1))

    # Calcula la probabilidad
    probability = binomial_coefficient * \
        (p_pascal ** r_pascal) * ((1 - p_pascal) ** x)

    return probability


def funcion_densidad_binomial():
    return


uniform_data = generador_uniforme_MR()
plot_histogram_with_pdf(uniform_data, y_values_uniform, x_values_uniform, 50,
                        title='Histograma de Distribución Uniforme con MR')
