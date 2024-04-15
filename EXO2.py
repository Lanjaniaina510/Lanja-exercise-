def get_variables(expression):
	return sorted(set(filter(str.isalpha, expression)))


def evaluate(expression, var_dict):
	expression = expression.replace("+", " or ")
	expression = expression.replace(".", " and ")
	expression = expression.replace("!", " not ")
	expression = expression.replace("~", " not")
	for var, val in var_dict.items():
		expression = expression.replace(var, val)
	return eval(expression)


def get_minterms(expression):
	minterms = []
	variables = get_variables(expression)
	var_count = len(variables)
	tab = []
	for i in range(2 ** var_count):
		b = bin(i)[2:].zfill(var_count)
		tab.append(list(b))

	for c in tab:
		var_dict = dict(zip(variables, c))
		result = evaluate(expression, var_dict)
		if result == 1:
			minterms.append(c)
	return minterms


def get_prime_implicants(minterms):
	prime_implicants = []
	used = [0 for i in range(len(minterms))]
	for i in range(len(minterms)):
		for j in range(len(minterms)):
			if minterms[i] != minterms[j]:
				idxs = [k for k in range(len(minterms[i])) if (minterms[i][k] != minterms[j][k])]
				if len(idxs) == 1:
					tmp = minterms[i].copy()
					tmp[idxs[0]] = "*"
					used[i] = 1
					if tmp not in prime_implicants:
						prime_implicants.append(tmp)

	if used.count(0) == len(used):
		return []

	for u in range(len(used)):
		if used[u] == 0:
			prime_implicants.append(minterms[u])

	return prime_implicants


def get_subset(implicant):
	subset = []
	star_count = implicant.count("*")
	tab = []
	for i in range(2 ** star_count):
		b = list(bin(i)[2:].zfill(star_count))
		tab.append(b)

	for t in tab:
		star_counter = 0
		tmp = implicant.copy()
		for i in range(len(tmp)):
			if implicant[i] == "*":
				tmp[i] = t[star_counter]
				star_counter += 1
		subset.append(tmp)
	return subset


def get_all_subsets(implicants):
	all_minterms = []
	for implicant in implicants:
		all_minterms.append(get_subset(implicant))

	return all_minterms


def get_all_minterms(subsets):
	all_minterms = []
	for subset in subsets:
		for s in subset:
			if s not in all_minterms:
				all_minterms.append(s)
	all_minterms = sorted(all_minterms)
	return all_minterms


def minimize(expression):
	minterms = get_minterms(expression)
	variables = get_variables(expression)
	prime_implicants = get_prime_implicants(minterms)
	while len(prime_implicants) != 0:
		minterms.clear()
		minterms.extend(prime_implicants)
		prime_implicants = get_prime_implicants(prime_implicants)
	subsets = get_all_subsets(minterms)
	all_minterms = get_all_minterms(subsets)

	redundant_indexes = []
	for i in range(len(subsets)):
		tmp_subsets = []
		for j in range(len(subsets)):
			if (i != j) and (j not in redundant_indexes):
				tmp_subsets.append(subsets[j])
		if get_all_minterms(tmp_subsets) == all_minterms:
			redundant_indexes.append(i)

	for idx in reversed(range(len(redundant_indexes))):
		del minterms[redundant_indexes[idx]]

	output = str()
	for i in range(len(minterms)):
		for j in range(len(minterms[i])):
			if minterms[i][j] == "1":
				output += variables[j]
			elif minterms[i][j] == "0":
				output += variables[j] + "\u0304"
			else:
				continue
			output += "."
		if output[-1] == ".":
			output = output[:-1]
		if i < len(minterms) - 1:
			output += " + "

	return output


def main():
	expression = input("Entrez l'expression à simplifier: ")
	print("Résultat:")
	output = minimize(expression)
	print("\t", output)


if __name__ == "__main__":
	main()
