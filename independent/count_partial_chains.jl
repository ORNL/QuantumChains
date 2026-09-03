# count_partial_chain.jl
# (c) Ryan Bennink 2025

# Lower-bound the logical error of a rotated surface code

# Qubits lie on a d×d square lattice (d odd).
# Only X errors are considered.
# Assuming an ideal maximum likelihood decoder,
# 	- Fewer than d/2 errors will always be decoded correctly
#  - More than d/2 errors lying on a top-to-bottom chain will be decoded incorrectly (=> logical error)
# Thus, the number of configurations of d′=(d+1)/2 chain-like errors is a lower bound
# on the number of configurations that result in logical Z error.
# Multiplying by p^d′ * (1-p)^(d^2-d′) yields a lower bound on the probability of
# a logical Z error.

# Main function
count_configs(d::Integer) = count_configs(d, div(d+1,2))

function count_configs(d::Integer, t::Integer)
	# Validate inputs
	d>0 && isodd(d) || error("d must be an odd whole number")
	d <= 67 || error("d must be ≤ 67 to avoid overflow")

	t < 0 && error("t must be >= 0")

	t == 0 && return 1

	# Lookup table for previously computed results (memoization).
	# (We could make this just a d×d×t array, at the cost of taking more space)
	memo = Matrix{Vector{Int128}}(undef, (d,d));
	for r in 1:d
		for c in 1:d
			memo[r,c] = zeros(Int128, 1 + min(r,t) - max(1, r+t-d))
		end
	end

	# Enumerate all the configurations
	num = Int128(0)
	for r in t:d		# loop over row of first error
		for c in 1:d	# loop over column of first error
			num += count_configs(d, t, t, (r,c), memo)
		end
	end

	return num
end

# Counts the number of configurations of t errors, the first of which is at (r,c)
# and the remainder of which are in the downward cone from (r,c)
function count_configs(d, tmax, t, (r,c), memo)

	# Only 1 way to arrange 1 error 
	t==1 && return Int128(1)
	
	# If we have computed this before, return the answer
	it = t - max(1,r+tmax-d) + 1
	if memo[r,c][it] > 0
		return memo[r,c][it]
	end

	# First time here.  Compute the answer
	num = Int128(0)
	for r_ in max(t-1,1):r-1					# loop over row of next error
		for c_ in colrange(d, (r,c), r_)		# loop over column of next error
			num += count_configs(d, tmax, t-1, (r_,c_), memo)
		end
	end

	# Save the result in lookup table
	memo[r,c][it] = num

	return num
end

# Return a range of column indices for row r_ of the "cone" rooted at (r,c)
function colrange(d, (r,c), r_)
	k = r - r_
	k > 0 || error("r_ must be less than r")
	if isodd(r+c)
		lo = c - k
		hi = c + k - 1
	else
		lo = c - k + 1
		hi = c + k
	end

	return max(lo,1):min(hi,d)
end

# Example usage:
if abspath(PROGRAM_FILE) == @__FILE__
	d = 67
	t = div(d+1,2)
	num = count_configs(d,t)
	println("d=$d, t=$t, num configurations = $num")
	# rerunning for timing
	@time num = count_configs(d,t)
	println("d=$d, t=$t, num configurations = $num")
end