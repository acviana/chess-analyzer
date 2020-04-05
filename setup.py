from distutils.core import setup

setup(
    name="Chess_Analyzer",
    version="0.1dev",
    packages=["chess_analyzer"],
    license="MIT License",
    install_requires=[
        'Click',
    ],
    entry_points="""
        [console_scripts]
        chess-analyzer=chess_analyzer.click:download
    """
)
