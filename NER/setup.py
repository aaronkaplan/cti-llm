from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()
version = '0.0.2'
setup(
    name='cyner',
    packages=find_packages(exclude=["tests", "models"]),
    version=version,
    license='MIT',
    description='Cybersecurity named entity recognition with LLM',
    url='https://github.com/aaronkaplan/cti-llm',
    #download_url="https://github.com/aiforsec/CyNER/archive/{}.tar.gz".format(version),
    keywords=['ner', 'nlp', 'language-model'],
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Paolo',
    author_email='paolo@priam.ai',
    classifiers=[
        'Development Status :: 4 - Beta',       # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    ],
    include_package_data=True,
    # test_suite='tests',
    install_requires=[
        'flair',
        'spacy',
        'ipywidgets',
        'spacy-transformers',
        'toml',
        'tensorboard',
        'torch',
        'transformers',
        'sentencepiece',
        'seqeval',
        'segtok',
        'sudachipy',
        'sudachidict_core'
    ],
    python_requires='>=3.10',
)