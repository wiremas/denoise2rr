# denoise2rr
kde desktop service for submitter imagesequences to Royal Render to denoise
with RenderMan's denoiser.

# install
- copy the ``prman_Densoise.desktop`` to ``~/.kde/share/kde4/services``
- change ``Exec=python /path/to/denoise2rr.py %F`` to point it to the correct
  path

# usage

- select the "variance" imagesequence
- right-click > "actions" > "PrManDenoise"

The script expects the following input:
- the "variance" image sequence which guides the denoising prodess with the
  following naming convention:
  <filename>_<frame>_variance.exr
- the image sequence that will be denoised with the following naming
  convention:
  <prefix>_<filename>_<frames>.exr
  The prefix parameter can be passed as an argument

The output will be formated as follows:
<prefix>_<filename>__filtered<frame>.exr
