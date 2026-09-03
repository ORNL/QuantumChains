# count_partial_chain_clusters.jl
# (c) Shaked Regev 2026

# Lower-bound the logical error of a rotated surface code

# Qubits lie on a d×d square lattice (d odd).
# Only X errors are considered.
# Assuming an ideal maximum likelihood decoder,
# 	- Fewer than d/2 errors will always be decoded correctly
#  - More than d/2 errors lying on a top-to-bottom chain will be decoded incorrectly (=> logical error)
# Thus, the number of configurations of d′=(d+1)/2 chain-like errors is a lower bound
# on the number of configurations that result in logical Z error.

# Main function
count_configs(d::Integer) = count_configs(d, div(d+1,2))

# Returns a Vector{Int128} of length t where result[k] = number of configurations
# of t chain-like errors that contain exactly k clusters of consecutive errors.
# A cluster is a maximal set of errors in consecutive rows.
function count_configs(d::Integer, t::Integer)
	# Validate inputs
	d>0 && isodd(d) || error("d must be an odd whole number")
	d <= 67 || error("d must be ≤ 67 to avoid overflow")
	t < 0 && error("t must be >= 0")
	t == 0 && return Int128[]

	# Lookup table for previously computed results (memoization).
	# memo[r,c] is a Matrix of size (it_size × t):
	#   rows index the same `it` as before, columns index cluster count 1..t.
	memo = Matrix{Matrix{Int128}}(undef, d, d)
	for r in 1:d
		for c in 1:d
			it_size = 1 + min(r,t) - max(1, r+t-d)
			memo[r,c] = zeros(Int128, it_size, t)
		end
	end

	# Enumerate all configurations
	result = zeros(Int128, t)
	for r in t:d		# loop over row of first error
		for c in 1:d	# loop over column of first error
			result .+= count_configs(d, t, t, (r,c), memo)
		end
	end

	return result
end

# Returns a Vector{Int128} of length tmax where v[k] = number of configurations
# of t errors, the first of which is at (r,c), with exactly k clusters total.
function count_configs(d, tmax, t, (r,c), memo)

	# Only 1 way to arrange 1 error, and it always forms exactly 1 cluster
	if t == 1
		v = zeros(Int128, tmax)
		v[1] = 1
		return v
	end

	# If we have computed this before, return the cached result
	it = t - max(1,r+tmax-d) + 1
	cached = @view memo[r,c][it, :]
	if any(>(0), cached)
		return cached
	end

	# First time here. Compute the answer.
	result = zeros(Int128, tmax)
	for r_ in max(t-1,1):r-1					# loop over row of next error
		for c_ in colrange(d, (r,c), r_)		# loop over column of next error
			sub = count_configs(d, tmax, t-1, (r_,c_), memo)
			if r_ == r - 1
				# Adjacent rows: (r,c) extends the sub-chain's first cluster.
				# Cluster count is unchanged.
				result .+= sub
			else
				# Gap between rows: (r,c) starts a new cluster.
				# Cluster count increases by 1, so shift sub up by one index.
				@views result[2:end] .+= sub[1:end-1]
			end
		end
	end

	# Save the result in lookup table
	memo[r,c][it, :] .= result

	return @view memo[r,c][it, :]
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
	if length(ARGS) < 1
		error("Usage: julia count_partial_chains_clusters.jl <d>")
	end
	d = parse(Int, ARGS[1])
	t = div(d+1,2)
	result = count_configs(d, t)

	filename = "configs_d$(d)_t$(t).csv"
	open(filename, "w") do f
		println(f, "num_clusters,num_configurations")
		for k in 1:t
			println(f, "$k,$(result[k])")
		end
	end
	println("Wrote $filename")
	println("Total configurations: $(sum(result))")

	# Rerun for timing
	@time result = count_configs(d, t)
end