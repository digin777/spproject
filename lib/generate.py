def generate(no):
	sp_arr=[4,1]
	my_ar=[1,4,1]
	count=2
	while len(my_ar)<=no:
		if len(my_ar)==no:
			break
		if count%2==0:
			my_ar[count]+=1
			count+=1
		else:
			my_ar.extend(sp_arr)
			count=len(my_ar)-1
	return(my_ar[:no])

if __name__ == '__main__':
	print(generate(81))
