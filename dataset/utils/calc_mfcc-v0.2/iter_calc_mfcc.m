function iter_calc_mfcc(indir)
  files = dir([indir '/*.wav']);
  for file = files'
      infile = [indir '/' file.name];
      outfile = [indir '/' file.name '.mfcc'];
      outspec = [indir '/' file.name '.spec'];
      [infile '  ' outfile '  ' outspec]
      #wavread(infile);
      calc_mfcc(infile, outfile, outspec)
  end
