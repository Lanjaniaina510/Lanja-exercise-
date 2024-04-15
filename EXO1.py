def evaluate(expression, variables_dict):
	# Remplacer chaque symbole par l'opérateur associé
	expression = expression.replace("+", " or ")
	expression = expression.replace(".", " and ")
	expression = expression.replace("!", " not ")
	expression = expression.replace("~", " not ")

	# Remplacer chaque variable par la valeur qui lui est associée dans le dictionnaire
	for variable, value in variables_dict.items():
		expression = expression.replace(variable, str(value))

	# Évaluer l'expression
	return eval(expression)


def get_variables(expression):
	# Renvoi l'ensemble des variables trouvées dans l'expression sans répétition et dans l'ordre alphabétique
	return sorted(set(filter(str.isalpha, expression)))


def truth_table(expression):
	# Modifier l'expression pour ignorer les minuscules et les espaces
	expression = expression.upper()

	# Liste contenant les résultats
	results = []
	variables = get_variables(expression)
	var_count = len(variables)
	print(" | ".join(variables + ["" + expression]))  # Affiche une en-tête
	print("-" * (len(expression) + 3 * (len(variables) + 2)))

	tab = []
	for i in range(2 ** var_count):
		b = list(bin(i)[2:].zfill(var_count))
		tab.append(b)

	# Évaluer l'expression pour chaque combinaison de 0 et de 1 sachant que l'on a n variable dans la fonction
	for values in tab:
		value_dict = dict(zip(variables, values))  # Dictionnaire des {variable: valeur}
		result = evaluate(expression, value_dict)  # Résultat
		results.append(result)  # Ajouter à la liste
		value_str = " | ".join(str(v) for v in values)  # Affiche la ligne correspondante à l'opération
		print(f" | ".join([value_str, str(int(result))]))

	return results, variables  # Renvoi la liste des résultats et des variables


def disjonctive_canon(results, variables):
	var_count = len(variables)
	tab = []
	for i in range(2 ** var_count):
		b = list(bin(i)[2:].zfill(var_count))
		tab.append(b)

	output = str()
	for i in range(len(tab)):
		if results[i] == 1:
			tmp = str()
			for j in range(len(tab[i])):
				if tab[i][j] == '1':
					tmp += variables[j]
				elif tab[i][j] == '0':
					tmp += variables[j] + "\u0304"
				tmp += "."
			if tmp[-1] == ".":
				tmp = tmp[:-1]
			tmp += " + "
			output += tmp

	if output[-3:] == " + ":
		output = output[:-3]

	return output


def conjonctive_canon(results, variables):
	# Presque identique à disjonctive_canon
	var_count = len(variables)
	tab = []
	for i in range(2 ** var_count):
		b = list(bin(i)[2:].zfill(var_count))
		tab.append(b)

	output = str()
	for i in range(len(tab)):
		if results[i] == 0:
			tmp = "("
			for j in range(len(tab[i])):
				if tab[i][j] == '1':
					tmp += variables[j] + "\u0304"
				elif tab[i][j] == '0':
					tmp += variables[j]
				tmp += " + "
			if tmp[-3:] == " + ":
				tmp = tmp[:-3]
			tmp += ")."
			output += tmp

	if output[-1] == ".":
		output = output[:-1]
	return output


def main():
	expression = input("Entrez l'expression de votre fonction (ex: A + !(B.C)): ")
	print("\nTable de vérité")
	results, variables = truth_table(expression)

	print("\nForme canonique disjonctive:")
	print("\t", disjonctive_canon(results, variables))
	print("\nForme canonique conjonctive:")
	print("\t", conjonctive_canon(results, variables))


if __name__ == "__main__":
	main()
