import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

class FilePreviewTile extends StatelessWidget {
  final PlatformFile file;

  const FilePreviewTile({super.key, required this.file});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 4),
      child: ListTile(
        leading: _getFileIcon(file.extension),
        title: Text(file.name),
        subtitle: Text('${(file.size / 1024 / 1024).toStringAsFixed(2)} MB'),
        trailing: IconButton(
          icon: const Icon(Icons.delete, color: Colors.red),
          onPressed: () {
            // In real app, you'd manage state via callback
          },
        ),
      ),
    );
  }

  Widget _getFileIcon(String? ext) {
    if (ext == null) return const Icon(Icons.insert_drive_file);
    switch (ext.toLowerCase()) {
      case 'pdf':
        return const Icon(Icons.picture_as_pdf, color: Colors.red);
      case 'doc':
      case 'docx':
        return const Icon(Icons.article, color: Colors.blue);
      case 'jpg':
      case 'jpeg':
      case 'png':
        return const Icon(Icons.image, color: Colors.purple);
      default:
        return const Icon(Icons.insert_drive_file);
    }
  }
}
