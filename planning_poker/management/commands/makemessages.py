import os

from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import CommandError
from django.core.management.commands import makemessages
from django.core.management.commands.makemessages import NO_LOCALE_DIR, STATUS_OK, write_pot_file
from django.core.management.utils import popen_wrapper


class Command(makemessages.Command):

    def handle(self, *args, **options):
        if options.get('domain') == 'djangojs':
            if 'vue' in options.get('extensions'):
                options['ignore_patterns'] += ['node_modules']
        super().handle(*args, **options)

    def process_locale_dir(self, locale_dir, files):
        """
        Extract translatable literals from the specified files, creating or
        updating the POT file for a given locale directory.
        Use the xgettext GNU gettext utility.
        """
        build_files = []
        for translatable in files:
            if self.verbosity > 1:
                self.stdout.write('processing file %s in %s\n' % (
                    translatable.file, translatable.dirpath
                ))
            if self.domain not in ('djangojs', 'django'):
                continue
            build_file = self.build_file_class(self, self.domain, translatable)
            try:
                build_file.preprocess()
            except UnicodeDecodeError as e:
                self.stdout.write(
                    'UnicodeDecodeError: skipped file %s in %s (reason: %s)' % (
                        translatable.file, translatable.dirpath, e,
                    )
                )
                continue
            build_files.append(build_file)

        if self.domain == 'djangojs' and ('.vue' in self.extensions):
            args = [
                os.path.join(os.path.dirname(settings.BASE_DIR), 'node_modules', '.bin', 'xgettext-vue'),
                '--output=-'
            ]
        elif self.domain == 'djangojs':
            is_templatized = build_file.is_templatized
            args = [
                'xgettext',
                '-d', self.domain,
                '--language=%s' % ('C' if is_templatized else 'JavaScript',),
                '--keyword=gettext_noop',
                '--keyword=gettext_lazy',
                '--keyword=ngettext_lazy:1,2',
                '--keyword=pgettext:1c,2',
                '--keyword=npgettext:1c,2,3',
                '--output=-',
            ]
        elif self.domain == 'django':
            args = [
                'xgettext',
                '-d', self.domain,
                '--language=Python',
                '--keyword=gettext_noop',
                '--keyword=gettext_lazy',
                '--keyword=ngettext_lazy:1,2',
                '--keyword=ugettext_noop',
                '--keyword=ugettext_lazy',
                '--keyword=ungettext_lazy:1,2',
                '--keyword=pgettext:1c,2',
                '--keyword=npgettext:1c,2,3',
                '--keyword=pgettext_lazy:1c,2',
                '--keyword=npgettext_lazy:1c,2,3',
                '--output=-',
            ]
        else:
            return

        input_files = [bf.work_path for bf in build_files]
        with NamedTemporaryFile(mode='w+') as input_files_list:
            input_files_list.write(('\n'.join(input_files)))
            input_files_list.flush()
            args.extend(['--files-from', input_files_list.name])
            args.extend(self.xgettext_options)
            msgs, errors, status = popen_wrapper(args)

        if errors:
            if status != STATUS_OK:
                for build_file in build_files:
                    build_file.cleanup()
                raise CommandError(
                    'errors happened while running xgettext on %s\n%s' %
                    ('\n'.join(input_files), errors)
                )
            elif self.verbosity > 0:
                # Print warnings
                self.stdout.write(errors)

        if msgs:
            if locale_dir is NO_LOCALE_DIR:
                file_path = os.path.normpath(build_files[0].path)
                raise CommandError(
                    'Unable to find a locale path to store translations for '
                    'file %s' % file_path
                )
            for build_file in build_files:
                msgs = build_file.postprocess_messages(msgs)
            potfile = os.path.join(locale_dir, '%s.pot' % self.domain)
            write_pot_file(potfile, msgs)

        for build_file in build_files:
            build_file.cleanup()
