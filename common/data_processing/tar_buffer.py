import io
import tarfile


def merge_to_buffered_tar(buffers):
    outer_tar_buffer = io.BytesIO()
    tar = tarfile.TarFile(mode="w", fileobj=outer_tar_buffer)
    for model in buffers:
        model_class = model[0]
        model_type = model[1]
        model_bin = io.BytesIO(model[2])
        info = tarfile.TarInfo(name=f"{model_class}_{model_type}.pth.tar")
        info.size = len(model_bin.read())
        model_bin.seek(0)
        tar.addfile(tarinfo=info, fileobj=model_bin)
    tar.close()
    outer_tar_buffer.seek(0)
    return outer_tar_buffer
