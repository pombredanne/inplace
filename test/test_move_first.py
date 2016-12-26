from   __future__        import print_function
import os
import pytest
from   inplace           import InPlace, DoubleOpenError
from   test_inplace_util import TEXT, pylistdir

def test_move_first_nobackup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with InPlace(str(p), move_first=True) as fp:
        assert not fp.closed
        for line in fp:
            fp.write(line.swapcase())
        assert not fp.closed
    assert fp.closed
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT.swapcase()

def test_move_first_backup_ext(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with InPlace(str(p), backup_ext='~', move_first=True) as fp:
        for line in fp:
            fp.write(line.swapcase())
    assert pylistdir(tmpdir) == ['file.txt', 'file.txt~']
    assert p.new(ext='txt~').read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_backup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    bkp = tmpdir.join('backup.txt')
    with InPlace(str(p), backup=str(bkp), move_first=True) as fp:
        assert not fp.closed
        for line in fp:
            fp.write(line.swapcase())
        assert not fp.closed
    assert fp.closed
    assert pylistdir(tmpdir) == ['backup.txt', 'file.txt']
    assert bkp.read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_error_backup_ext(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with pytest.raises(RuntimeError):
        with InPlace(str(p), backup_ext='~', move_first=True) as fp:
            for i, line in enumerate(fp):
                fp.write(line.swapcase())
                if i > 5:
                    raise RuntimeError("I changed my mind.")
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT

def test_move_first_pass_nobackup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with InPlace(str(p), move_first=True):
        pass
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == ''

def test_move_first_delete_nobackup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with InPlace(str(p), move_first=True) as fp:
        for i, line in enumerate(fp):
            fp.write(line.swapcase())
            if i == 5:
                p.remove()
    assert pylistdir(tmpdir) == []

def test_move_first_delete_backup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    bkp = tmpdir.join('backup.txt')
    with InPlace(str(p), backup=str(bkp), move_first=True) as fp:
        for i, line in enumerate(fp):
            fp.write(line.swapcase())
            if i == 5:
                p.remove()
    assert pylistdir(tmpdir) == ['backup.txt']
    assert bkp.read() == TEXT

def test_move_first_early_close_nobackup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with InPlace(str(p), move_first=True) as fp:
        for line in fp:
            fp.write(line.swapcase())
        fp.close()
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT.swapcase()

def test_move_first_early_close_and_write_nobackup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with pytest.raises(ValueError):
        with InPlace(str(p), move_first=True) as fp:
            for line in fp:
                fp.write(line.swapcase())
            fp.close()
            fp.write('And another thing...\n')
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT.swapcase()

def test_move_first_early_close_backup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    bkp = tmpdir.join('backup.txt')
    with InPlace(str(p), backup=str(bkp), move_first=True) as fp:
        for line in fp:
            fp.write(line.swapcase())
        fp.close()
    assert pylistdir(tmpdir) == ['backup.txt', 'file.txt']
    assert bkp.read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_early_close_and_write_backup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    bkp = tmpdir.join('backup.txt')
    with pytest.raises(ValueError):
        with InPlace(str(p), backup=str(bkp), move_first=True) as fp:
            for line in fp:
                fp.write(line.swapcase())
            fp.close()
            fp.write('And another thing...\n')
    assert pylistdir(tmpdir) == ['backup.txt', 'file.txt']
    assert bkp.read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_rollback_nobackup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with InPlace(str(p), move_first=True) as fp:
        for line in fp:
            fp.write(line.swapcase())
        fp.rollback()
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT

def test_move_first_rollback_and_write_nobackup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with pytest.raises(ValueError):
        with InPlace(str(p), move_first=True) as fp:
            for line in fp:
                fp.write(line.swapcase())
            fp.rollback()
            fp.write('And another thing...\n')
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT

def test_move_first_rollback_backup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    bkp = tmpdir.join('backup.txt')
    with InPlace(str(p), backup=str(bkp), move_first=True) as fp:
        for line in fp:
            fp.write(line.swapcase())
        fp.rollback()
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT

def test_move_first_rollback_and_write_backup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    bkp = tmpdir.join('backup.txt')
    with pytest.raises(ValueError):
        with InPlace(str(p), backup=str(bkp), move_first=True) as fp:
            for line in fp:
                fp.write(line.swapcase())
            fp.rollback()
            fp.write('And another thing...\n')
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT

def test_move_first_overwrite_backup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    bkp = tmpdir.join('backup.txt')
    bkp.write('This is not the file you are looking for.\n')
    with InPlace(str(p), backup=str(bkp), move_first=True) as fp:
        for line in fp:
            fp.write(line.swapcase())
    assert pylistdir(tmpdir) == ['backup.txt', 'file.txt']
    assert bkp.read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_rollback_overwrite_backup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    bkp = tmpdir.join('backup.txt')
    bkp.write('This is not the file you are looking for.\n')
    with InPlace(str(p), backup=str(bkp), move_first=True) as fp:
        for line in fp:
            fp.write(line.swapcase())
        fp.rollback()
    assert pylistdir(tmpdir) == ['backup.txt', 'file.txt']
    assert bkp.read() == 'This is not the file you are looking for.\n'
    assert p.read() == TEXT

def test_move_first_prechdir_backup(tmpdir, monkeypatch):
    assert pylistdir(tmpdir) == []
    monkeypatch.chdir(tmpdir)
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with InPlace(str(p), backup='backup.txt', move_first=True) as fp:
        for line in fp:
            fp.write(line.swapcase())
    assert pylistdir(tmpdir) == ['backup.txt', 'file.txt']
    assert tmpdir.join('backup.txt').read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_midchdir_backup(tmpdir, monkeypatch):
    """
    Assert that changing directory between creating an InPlace object and
    opening it works
    """
    filedir = tmpdir.mkdir('filedir')
    wrongdir = tmpdir.mkdir('wrongdir')
    p = filedir.join("file.txt")
    p.write(TEXT)
    monkeypatch.chdir(filedir)
    fp = InPlace('file.txt', backup='backup.txt', delay_open=True, move_first=True)
    monkeypatch.chdir(wrongdir)
    assert fp.closed
    with fp:
        assert not fp.closed
        for line in fp:
            fp.write(line.swapcase())
        assert not fp.closed
    assert fp.closed
    assert os.getcwd() == str(wrongdir)
    assert pylistdir(wrongdir) == []
    assert pylistdir(filedir) == ['backup.txt', 'file.txt']
    assert filedir.join('backup.txt').read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_postchdir_backup(tmpdir, monkeypatch):
    """ Assert that changing directory after opening an InPlace object works """
    filedir = tmpdir.mkdir('filedir')
    wrongdir = tmpdir.mkdir('wrongdir')
    p = filedir.join("file.txt")
    p.write(TEXT)
    monkeypatch.chdir(filedir)
    with InPlace('file.txt', backup='backup.txt', move_first=True) as fp:
        monkeypatch.chdir(wrongdir)
        for line in fp:
            fp.write(line.swapcase())
    assert os.getcwd() == str(wrongdir)
    assert pylistdir(wrongdir) == []
    assert pylistdir(filedir) == ['backup.txt', 'file.txt']
    assert filedir.join('backup.txt').read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_different_dir_backup(tmpdir, monkeypatch):
    monkeypatch.chdir(tmpdir)
    filedir = tmpdir.mkdir('filedir')
    bkpdir = tmpdir.mkdir('bkpdir')
    p = filedir.join("file.txt")
    p.write(TEXT)
    with InPlace(
        os.path.join('filedir', 'file.txt'),
        backup=os.path.join('bkpdir', 'backup.txt'),
        move_first=True,
    ) as fp:
        for line in fp:
            fp.write(line.swapcase())
    assert pylistdir(filedir) == ['file.txt']
    assert pylistdir(bkpdir) == ['backup.txt']
    assert bkpdir.join('backup.txt').read() == TEXT
    assert p.read() == TEXT.swapcase()

def test_move_first_backup_dirpath(tmpdir):
    """
    Assert that using a path to a directory as the backup path raises an error
    when closing
    """
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    not_a_file = tmpdir.join('not-a-file')
    not_a_file.mkdir()
    assert pylistdir(not_a_file) == []
    fp = InPlace(str(p), backup=str(not_a_file), move_first=True)
    fp.write(u'This will be discarded.\n')
    with pytest.raises(EnvironmentError):
        fp.close()
    assert pylistdir(tmpdir) == ['file.txt', 'not-a-file']
    assert p.read() == TEXT
    assert pylistdir(not_a_file) == []

def test_move_first_backup_nosuchdir(tmpdir):
    """
    Assert that using a path to a file in a nonexistent directory as the backup
    path raises an error when opening
    """
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    fp = InPlace(
        str(p),
        backup=str(tmpdir.join('nonexistent', 'backup.txt')),
        move_first=True,
        delay_open=True,
    )
    with pytest.raises(EnvironmentError):
        fp.open()
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT

def test_move_first_double_open_nobackup(tmpdir):
    assert pylistdir(tmpdir) == []
    p = tmpdir.join("file.txt")
    p.write(TEXT)
    with InPlace(str(p), move_first=True) as fp:
        with pytest.raises(DoubleOpenError):
            fp.open()
        assert not fp.closed
        for line in fp:
            fp.write(line.swapcase())
        assert not fp.closed
    assert fp.closed
    assert pylistdir(tmpdir) == ['file.txt']
    assert p.read() == TEXT.swapcase()
