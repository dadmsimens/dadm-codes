function error1 = calculate_error(ref, reconstructed, mask, norm_type)

er = abs(ref - reconstructed) .* mask;
err = er(er > 0);
error1 = norm(err(:), norm_type);

