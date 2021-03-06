function calc_mfcc(infile, outfile, outfilespec, verbose)
% calc_mfcc(infile, outfile)
%   Emulate HTK MFCC calculation as best as possible
% 2013-02-26 Dan Ellis dpwe@ee.columbia.edu

if nargin < 4;  verbose = 0; end

VERSION = 0.2;
DATE = 20130624;

if verbose
  disp(['*** calc_mfcc v', num2str(VERSION), ' of ', num2str(DATE), ...
        ' ***']);
end

#[d,sr] = audioread(infile);
[d,sr] = wavread(infile);
% This is how HTK sees the samepls
d = (32768*d);
[mfc,as,ps] = melfcc(d, sr, 'lifterexp', -22, 'nbands', 26, ...
             'dcttype', 3, 'maxfreq',8000, 'fbtype', 'htkmel', ...
             'sumpower', 1);

#writeasc(outfile, mfc');
#writeasc(outfilespec, ps');

save("-hdf5", outfilespec, 'ps');
