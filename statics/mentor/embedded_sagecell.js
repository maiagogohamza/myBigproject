<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>blah YourTitleGoesHere, for the first time</title>
<script src="https://sagecell.sagemath.org/static/jquery.min.js"></script>
<script src="https://sagecell.sagemath.org/embedded_sagecell.js"></script>
<script>
$(function () {
// Make *any* div with class ’compute’ a Sage cell
sagecell.makeSagecell({inputLocation: ’div.compute’,
template:
sagecell.templates.minimal,
evalButtonText: ’Launch the Interactive Applet Now’});
});
</script>
</head>
<body style="width: 1000px;">
<! you may start modifying below this point!>
<! you may start modifying below this point!>
<! you may start modifying below this point!>
<h1>blah YourTitleGoesHere, for the second time</h1>
<p>An Interactive Applet powered by Sage and MathJax.</p>
<p>(By YourNameGoesHere)</p>
<hr>
<h2>Overview</h2>
<p>blah blah blah</p>
<p>yada yada yada</p>
<p>blah blah blah</p>
<h2>Instructions</h2>
<p>blah blah blah</p>
<p>yada yada yada</p>
<div class="compute">
<script type="text/x-sage">
f(x) = x^3 - x
df(x) = diff(f(x), x)
@interact
def tangent_at_point(x0 = slider(-2, 2, 0.1, -1.5, label='x-coordinate')):
    """
    Shows the tangent line at the point x0,
    using f and its derivative as global variables.
    """
    y0 = f(x0)
    slope = df(x0)
    # y - y0 = slope*(x - x0) implies
    # y = slope*x - slope*x0 + y0
    b = y0 - slope*x0
    P1 = plot(f, -2, 2, color='blue', ymin=-6, ymax=6, gridlines='minor')
    P2 = plot(slope*x + b, -2, 2, color='tan', ymin=-6, ymax=6)
    P3 = point((x0, y0), color='red', size=50)
    P = P1+P2+P3
    P.show(figsize=3)

    return

</script>
</div>
<h2>Discussion</h2>
<p>blah blah blah</p>
<p>yada yada yada</p>
<p>blah blah blah</p>
<hr>
Last modified on PutTheDateHere.
</body>
</html>